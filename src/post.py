"""Orquestrador: gera 1 post (card visual + legenda) e publica nas plataformas.

Executado uma vez por disparo do agendador (GitHub Actions). Rodando 20 vezes ao
dia, produz 20 posts/dia — sem manter estado entre execuções.

Uso:
    python -m src.post [--type motivacional|mercado|educacional] [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import tempfile
from datetime import datetime, timedelta, timezone

from . import config, generate, history, market
from .publishers import instagram, threads


def _current_slot() -> int:
    """Índice do horário agendado (SCHEDULE_BRT) mais próximo de agora (Brasília)."""
    brt = timezone(timedelta(hours=config.BRT_OFFSET_HOURS))
    now = datetime.now(brt)
    minutes = now.hour * 60 + now.minute
    diffs = [abs(minutes - (h * 60 + m)) for h, m in config.SCHEDULE_BRT]
    return diffs.index(min(diffs))


def _day_of_year() -> int:
    brt = timezone(timedelta(hours=config.BRT_OFFSET_HOURS))
    return datetime.now(brt).timetuple().tm_yday


def _slot_plan(slot: int) -> tuple[str, str | None]:
    """Formato/ativo de um slot: 2 slots são mercado (ouro/Nasdaq); o resto revezam."""
    if slot == config.GOLD_SLOT_INDEX:
        return "mercado", "ouro"
    if slot == config.NASDAQ_SLOT_INDEX:
        return "mercado", "nasdaq"
    rotation = config.TRADER_FORMATS_ROTATION
    return rotation[(slot + _day_of_year()) % len(rotation)], None


def plan_post(content_type: str | None) -> tuple[str, str | None]:
    """Decide (formato, ativo) para um disparo MANUAL forçado (--type / workflow_dispatch)."""
    ct = content_type or config.POST_TYPE
    if ct == "mercado":
        return "mercado", random.choice(list(market.MARKET_ASSETS))
    if ct in config.TRADER_FORMATS_ROTATION:  # formato específico forçado
        return ct, None
    return _slot_plan(_current_slot())  # "trader" ou vazio → pelo horário atual


def _posts_today() -> int:
    """Quantos posts já foram publicados hoje (Brasília), lendo a memória."""
    today = datetime.now(timezone(timedelta(hours=config.BRT_OFFSET_HOURS))).date().isoformat()
    return sum(1 for e in history._load(history.HISTORY_PATH) if str(e.get("date", "")).startswith(today))


def _due_slot() -> int | None:
    """O próximo slot 'devendo': o de índice = nº de posts de hoje, se seu horário já chegou.

    Torna o sistema à prova de atraso do agendador: cada disparo publica no máximo
    um post — o próximo da fila — e só depois do horário previsto do slot. Assim não
    posta de madrugada, não junta vários no mesmo minuto e não passa de 20/dia.
    """
    count = _posts_today()
    if count >= len(config.SCHEDULE_BRT):
        return None  # cota diária atingida
    slot = count
    h, m = config.SCHEDULE_BRT[slot]
    now = datetime.now(timezone(timedelta(hours=config.BRT_OFFSET_HOURS)))
    if now.hour * 60 + now.minute < h * 60 + m:
        return None  # horário do próximo slot ainda não chegou
    return slot


def _angle(fmt: str, slot: int) -> str | None:
    """Tema (ângulo) do post, variando por (slot + dia) para não repetir."""
    if fmt == "mercado":
        return random.choice(config.MARKET_ANGLES)
    return config.TRADER_ANGLES[(slot + _day_of_year()) % len(config.TRADER_ANGLES)]


def run(content_type: str | None = None, dry_run: bool | None = None) -> None:
    dry_run = config.DRY_RUN if dry_run is None else dry_run
    forced = content_type or config.POST_TYPE  # disparo manual com formato específico

    if forced:
        fmt, asset_key = plan_post(forced)
        _post_one(_current_slot(), fmt, asset_key, dry_run)
        return

    # Automático: recupera vários horários atrasados de uma vez (até CATCHUP_MAX),
    # para chegar perto dos 20/dia mesmo que o GitHub dispare poucas vezes.
    published = 0
    errors: list[str] = []
    for _ in range(1 if dry_run else config.CATCHUP_MAX):
        slot = _due_slot()
        if slot is None:
            break
        fmt, asset_key = _slot_plan(slot)
        try:
            _post_one(slot, fmt, asset_key, dry_run)
            published += 1
        except SystemExit as exc:  # falha de publicação de um post — segue tentando os demais
            errors.append(str(exc))
            break
        if dry_run:
            break

    if published == 0 and not dry_run and not errors:
        print("Nada a postar agora (fora da janela, horário do próximo slot ainda "
              "não chegou, ou cota diária de 20 já atingida).")
    if errors:
        raise SystemExit("Falhas de publicação:\n" + "\n".join(errors))


def _post_one(slot: int, fmt: str, asset_key: str | None, dry_run: bool) -> None:
    """Gera e publica UM post do slot informado. Levanta SystemExit se a publicação falhar."""
    asset = None
    snapshot = None
    if fmt == "mercado":
        asset = market.fetch_asset(asset_key)
        if not asset:  # se falhar o ativo, cai para foto-reflexão
            fmt = "foto"
        else:
            snapshot = market.asset_snapshot(asset)

    angle = _angle(fmt, slot)
    avoid = history.recent_headlines(20)  # memória: não repetir posts recentes
    result = generate.generate_post(fmt, snapshot, angle=angle, avoid=avoid)
    fmt = result["fmt"]  # pode ter caído de mercado para foto
    caption = result["caption"]

    print(f"[slot {slot}] [{fmt}] {result.get('main', '')}")
    print(f"legenda:\n{caption}\n")

    # Sempre gera o card visual. A semente varia paleta/cena por post.
    seed = slot + _day_of_year()
    out_path = "preview.png" if dry_run else os.path.join(tempfile.gettempdir(), "post_card.png")
    image_path = _build_card(result, asset, out_path, seed)

    if dry_run:
        print(f"DRY_RUN ativo — card salvo em {image_path}; nada publicado.")
        return

    if not config.PLATFORMS:
        print("Nenhuma plataforma configurada (PLATFORMS). Nada publicado.")
        return

    image_url = _host_image(image_path)
    if image_url is None:
        print("Aviso: não foi possível hospedar a imagem.", file=sys.stderr)

    errors = []
    for platform in config.PLATFORMS:
        try:
            if platform == "threads":
                if image_url:
                    post_id = threads.publish_image(image_url, caption)
                else:
                    post_id = threads.publish_text(caption)
            elif platform == "instagram":
                if not image_url:
                    raise RuntimeError("Instagram requer imagem (configure IMGBB_API_KEY).")
                post_id = instagram.publish_image(image_url, caption)
            else:
                print(f"Plataforma desconhecida ignorada: {platform}")
                continue
            print(f"Publicado em {platform}: {post_id}")
        except Exception as exc:  # noqa: BLE001 — reportar por plataforma sem abortar as demais
            errors.append(f"{platform}: {exc}")
            print(f"Falha ao publicar em {platform}: {exc}", file=sys.stderr)

    if errors:
        raise SystemExit("Falhas de publicação:\n" + "\n".join(errors))

    # Registra na memória (o workflow commita o arquivo depois de publicar). Isso
    # também faz o próximo _due_slot() enxergar o post recém-feito no mesmo job.
    brt = timezone(timedelta(hours=config.BRT_OFFSET_HOURS))
    history.append(
        {
            "date": datetime.now(brt).isoformat(timespec="minutes"),
            "type": fmt,
            "angle": angle,
            "headline": result.get("main", ""),
        }
    )


def _build_card(result: dict, asset: dict | None, out_path: str, seed: int = 0) -> str:
    """Desenha o card conforme o formato do post."""
    from . import cards, image, imagegen

    fmt = result["fmt"]
    handle = config.POST_HANDLE

    # Formatos desenhados (sem foto de IA) — dão variedade ao feed.
    if fmt == "citacao":
        return cards.build_quote(result["statement"], handle, out_path, seed)
    if fmt == "lista":
        return cards.build_list(result["title"], result["items"], handle, out_path, seed)
    if fmt == "mito_verdade":
        return cards.build_myth_truth(result["mito"], result["verdade"], handle, out_path, seed)
    if fmt == "numero":
        return cards.build_number(result["stat"], result["label"], handle, out_path, seed)

    # Formatos com foto de IA: foto-reflexão e mercado.
    chart_img = None
    if fmt == "mercado" and asset:
        try:
            from . import chart

            chart_img = chart.render_candles(asset["candles"], asset["label"], asset["change"])
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: não foi possível gerar o gráfico: {exc}", file=sys.stderr)

    background = imagegen.generate_background("mercado" if fmt == "mercado" else "trader", seed)
    print("Fundo: imagem de IA." if background is not None else "Fundo: cena desenhada (sem IA).")
    badge = "mercado" if fmt == "mercado" else "trader"
    return image.build_card(
        result["headline"], badge, handle, out_path, chart_img, seed, background=background
    )


def _host_image(path: str) -> str | None:
    """Hospeda a imagem no GitHub (URL raw) SEM tocar no worktree nem no main.

    Usa plumbing do git (hash-object → mktree → commit-tree) para criar um commit
    isolado só com a imagem e faz force-push para o ref `media`. A URL raw é pinada
    no SHA do commit — pública e estável. Como não mexe no índice nem no main, não
    há rebase nem conflito de binário entre as 20 execuções diárias.
    """
    import subprocess
    import time as _time

    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        print("Aviso: fora do GitHub Actions — não é possível hospedar a imagem.", file=sys.stderr)
        return None

    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "github-actions[bot]",
        "GIT_AUTHOR_EMAIL": "github-actions[bot]@users.noreply.github.com",
        "GIT_COMMITTER_NAME": "github-actions[bot]",
        "GIT_COMMITTER_EMAIL": "github-actions[bot]@users.noreply.github.com",
    }

    def git(args, **kw):
        return subprocess.run(["git", *args], capture_output=True, text=True, env=env, **kw)

    try:
        blob = git(["hash-object", "-w", path]).stdout.strip()
        if not blob:
            return None
        tree = git(["mktree"], input=f"100644 blob {blob}\tcard.png\n").stdout.strip()
        commit = git(["commit-tree", tree, "-m", "card do post"]).stdout.strip()
        if not commit:
            return None
        for _ in range(4):
            if git(["push", "-f", "origin", f"{commit}:refs/heads/media"]).returncode == 0:
                return f"https://raw.githubusercontent.com/{repo}/{commit}/card.png"
            _time.sleep(2)
        print("Aviso: falha ao dar push da imagem para o ref media.", file=sys.stderr)
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: falha ao hospedar imagem no GitHub: {exc}", file=sys.stderr)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera e publica um post sobre trade.")
    parser.add_argument("--type", choices=("trader", *config.ALL_FORMATS), default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(content_type=args.type, dry_run=True if args.dry_run else None)


if __name__ == "__main__":
    main()
