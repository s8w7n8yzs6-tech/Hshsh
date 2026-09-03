"""Bot de DM: responde no direct quem comenta nos seus posts.

Usa o mecanismo oficial de "private reply" do Instagram (1 mensagem por
comentário, até 7 dias depois dele). É um bot SEPARADO do de postagem.

Travas anti-spam:
- nunca envia DM duas vezes para a mesma pessoa;
- ignora comentários da própria conta;
- limite de envios por rodada (DM_MAX_PER_RUN).

Uso:
    python -m src.dm [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import requests

from . import config

_BASE = "https://graph.instagram.com/v21.0"
STATE_PATH = os.path.join("state", "dm.json")
MAX_PER_RUN = int(os.getenv("DM_MAX_PER_RUN") or "15")
MEDIA_LIMIT = int(os.getenv("DM_MEDIA_LIMIT") or "8")

_FALLBACK = (
    "Opa, obrigado por comentar! 🙌 Fico feliz que o conteúdo tenha feito sentido. "
    "Se quiser trocar uma ideia sobre mercado, é só me chamar por aqui."
)


# ----------------------------------------------------------------- estado
def _load_state() -> dict:
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict):
            d.setdefault("comments", [])
            d.setdefault("users", [])
            return d
    except (OSError, ValueError):
        pass
    return {"comments": [], "users": []}


def _save_state(d: dict, max_items: int = 5000) -> None:
    d["comments"] = d["comments"][-max_items:]
    d["users"] = d["users"][-max_items:]
    os.makedirs(os.path.dirname(STATE_PATH) or ".", exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


# ------------------------------------------------------------------- API
def _get(path: str, params: dict) -> dict:
    params = {**params, "access_token": config.INSTAGRAM_ACCESS_TOKEN}
    r = requests.get(f"{_BASE}/{path}", params=params, timeout=30)
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} em GET {path}: {r.text[:300]}")
    return r.json()


def _me_username() -> str:
    try:
        return _get("me", {"fields": "username"}).get("username", "")
    except Exception:  # noqa: BLE001
        return ""


def recent_comments() -> list[dict]:
    """Comentários recentes dos últimos posts: [{id, text, username}]."""
    media = _get("me/media", {"fields": "id,timestamp", "limit": MEDIA_LIMIT}).get("data", [])
    out: list[dict] = []
    for m in media:
        try:
            cs = _get(f"{m['id']}/comments", {"fields": "id,text,username,timestamp", "limit": 50})
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: não foi possível ler comentários de {m['id']}: {exc}", file=sys.stderr)
            continue
        for c in cs.get("data", []):
            out.append({"id": c.get("id"), "text": (c.get("text") or "").strip(),
                        "username": (c.get("username") or "").strip()})
    return out


def send_private_reply(comment_id: str, text: str, timeout: int = 30) -> str:
    """Envia o DM respondendo a um comentário (private reply)."""
    r = requests.post(
        f"{_BASE}/{config.INSTAGRAM_USER_ID}/messages",
        json={
            "recipient": {"comment_id": comment_id},
            "message": {"text": text},
            "access_token": config.INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=timeout,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} em messages: {r.text[:300]}")
    return str(r.json().get("message_id") or r.json().get("id") or "ok")


# ------------------------------------------------------------- mensagem
def compose(comment_text: str, username: str) -> str:
    """Resposta curta e pessoal ao comentário (Claude). Cai no texto padrão se falhar."""
    try:
        import anthropic

        prompt = (
            "Você responde, pelo DIRECT do Instagram, uma pessoa que comentou num post "
            "sobre mercado financeiro/trading. Escreva uma resposta CURTA (máx ~300 "
            "caracteres), calorosa e natural, em português do Brasil, que:\n"
            "- agradeça e responda de verdade ao que a pessoa disse;\n"
            "- soe humana, nada de texto robótico ou de vendas;\n"
            "- convide a continuar a conversa, sem forçar.\n"
            "REGRAS: nunca dê recomendação de compra/venda, alvo de preço ou promessa "
            "de lucro; não prometa retorno; no máximo 1 emoji; não use hashtags.\n\n"
            f"Comentário de @{username}: \"{comment_text}\""
        )
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=300,
            thinking={"type": "disabled"},
            system="Você escreve DMs curtas, humanas e educadas em português do Brasil.",
            messages=[{"role": "user", "content": prompt}],
        )
        txt = "".join(b.text for b in resp.content if b.type == "text").strip()
        return txt[:900] or _FALLBACK
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: falha ao gerar a mensagem ({exc}); usando texto padrão.", file=sys.stderr)
        return _FALLBACK


# ------------------------------------------------------------------ run
def run(dry_run: bool = False) -> None:
    if not (config.INSTAGRAM_USER_ID and config.INSTAGRAM_ACCESS_TOKEN):
        raise SystemExit("Credenciais do Instagram ausentes.")

    state = _load_state()
    done_comments = set(state["comments"])
    done_users = set(state["users"])
    me = _me_username().lower()

    try:
        comments = recent_comments()
    except Exception as exc:  # noqa: BLE001
        # Sai limpo (sem falhar o job) enquanto a permissão de mensagens/comentários
        # não estiver liberada no app da Meta.
        print(f"Não foi possível ler os comentários: {exc}", file=sys.stderr)
        print("Verifique se o token tem as permissões instagram_business_manage_comments "
              "e instagram_business_manage_messages.")
        return
    print(f"{len(comments)} comentários lidos nos últimos {MEDIA_LIMIT} posts.")

    sent = 0
    for c in comments:
        cid, user, text = c["id"], c["username"], c["text"]
        if not cid or cid in done_comments:
            continue
        if not user or user.lower() == me:      # não responder a si mesmo
            done_comments.add(cid)
            continue
        if user.lower() in done_users:          # já falamos com essa pessoa
            done_comments.add(cid)
            continue
        if sent >= MAX_PER_RUN:
            print(f"Limite de {MAX_PER_RUN} DMs nesta rodada atingido.")
            break

        msg = compose(text, user)
        if dry_run:
            print(f"[DRY-RUN] @{user}: {text[:60]!r} -> {msg[:120]!r}")
        else:
            try:
                mid = send_private_reply(cid, msg)
                print(f"DM enviado para @{user} ({mid}).")
            except Exception as exc:  # noqa: BLE001
                print(f"Falha ao enviar DM para @{user}: {exc}", file=sys.stderr)
                continue
            time.sleep(2)  # respiro entre envios
        done_comments.add(cid)
        done_users.add(user.lower())
        sent += 1

    state["comments"] = sorted(done_comments)
    state["users"] = sorted(done_users)
    if not dry_run:
        _save_state(state)
    print(f"{sent} DM(s) {'simulado(s)' if dry_run else 'enviado(s)'}.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Responde no direct quem comenta nos posts.")
    ap.add_argument("--dry-run", action="store_true")
    run(dry_run=ap.parse_args().dry_run)


if __name__ == "__main__":
    main()
