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
    """Formato/ativo de um slot.

    Slots PARES = desenvolvimento (educativo): 2 são mercado (ouro/Nasdaq) e os
    demais revezam padrão/conceito/dica. Slots ÍMPARES = mentalidade. Resultado:
    10 educativos + 10 de mentalidade por dia, intercalados no feed.
    """
    day = _day_of_year()
    if slot == config.GOLD_SLOT_INDEX:
        return "mercado", "ouro"
    if slot == config.NASDAQ_SLOT_INDEX:
        return "mercado", "nasdaq"
    if slot % 2 == 0:  # educativo — o acervo (pool) decide o assunto, sem repetir
        return "edu", None
    ment = config.MENTALITY_FORMATS  # mentalidade
    return ment[((slot - 1) // 2 + day) % len(ment)], None


def plan_post(content_type: str | None) -> tuple[str, str | None]:
    """Decide (formato, ativo) para um disparo MANUAL forçado (--type / workflow_dispatch)."""
    ct = content_type or config.POST_TYPE
    if ct == "mercado":
        return "mercado", random.choice(list(market.MARKET_ASSETS))
    if ct in config.ALL_FORMATS:  # formato específico forçado
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


# Buscas de foto (grátis, CC0) para os formatos com imagem de fundo.
FOTO_QUERIES = [
    "stock market chart", "trading screen finance", "business office laptop",
    "financial graph screen", "businessman office window", "stock exchange building",
]

HISTORIA_EVERY = 5  # 1 a cada 5 posts educativos é uma HISTÓRIA (carrossel)


def _used_subjects() -> set:
    return {e.get("subject") for e in history._load(history.HISTORY_PATH) if e.get("subject")}


def _next_historia_subject(used: set) -> dict | None:
    """Próxima MANCHETE em alta do mercado/negócios do Brasil ainda não usada.

    Puxa as manchetes da semana (Google Notícias RSS) e devolve a primeira que
    ainda não virou post. Como as manchetes mudam sempre, o acervo se renova
    sozinho e nunca repete. Retorna None se não houver manchete disponível.
    """
    from . import news

    try:
        heads = news.fetch_headlines(25)
    except Exception:  # noqa: BLE001
        heads = []
    for h in heads:
        key = f"man:{h['slug']}"
        if key not in used:
            return {"key": key, "fmt": "historia", "badge": "MERCADO NO BRASIL",
                    "nome": h["title"], "hint": h.get("source", "")}
    return None


def _next_edu_subject(fmt: str | None = None) -> dict:
    """Próximo assunto educativo que AINDA NÃO foi usado (nunca repete).

    HISTÓRIAS (carrosséis de pessoas) aparecem 1 a cada HISTORIA_EVERY posts
    educativos e têm renovação automática do acervo de pessoas. Os demais formatos
    vêm do acervo de "aprender" (estratégias/indicadores/conceitos/dicas).
    """
    from . import patterns

    used = _used_subjects()
    want_historia = fmt == "historia" or (
        fmt is None
        and sum(1 for e in history._load(history.HISTORY_PATH) if e.get("subject")) % HISTORIA_EVERY == 0
    )
    if want_historia:
        subj = _next_historia_subject(used)
        if subj is not None:
            return subj
        # sem manchete disponível → cai para o acervo de "aprender"

    pool = patterns.build_pool()
    for item in pool:
        if fmt and item["fmt"] != fmt:
            continue
        if item["key"] not in used:
            return item
    for item in pool:  # acervo de aprender esgotado: recicla (centenas de posts depois)
        if not fmt or item["fmt"] == fmt:
            return item
    return pool[0]


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

    # Assunto do post. Formatos educativos ("edu" ou forçados) puxam o próximo
    # assunto do acervo que ainda não foi usado — assim NADA se repete.
    subject = None
    if fmt in ("edu", "historia", "conceito", "dica"):
        subject = _next_edu_subject(None if fmt == "edu" else fmt)
        fmt = subject["fmt"]

    if subject is not None:
        nome = (subject.get("nome") or "").strip()
        angle = f"{nome}: {subject['hint']}".strip(": ").strip() if nome else subject["hint"]
    else:
        angle = _angle(fmt, slot)

    avoid = history.recent_headlines(20)  # memória: não repetir posts recentes
    result = generate.generate_post(fmt, snapshot, angle=angle, avoid=avoid)
    fmt = result["fmt"]  # pode ter caído de mercado para foto
    if subject is not None:
        result["_subject"] = subject  # formato, badge e diagrama do assunto
    caption = result["caption"]

    print(f"[slot {slot}] [{fmt}] {result.get('main', '')}")
    print(f"legenda:\n{caption}\n")

    # Gera a(s) imagem(ns). Carrossel (história) vira vários slides; o resto, 1 card.
    seed = slot + _day_of_year()
    image_paths = _build_media(result, asset, seed, dry_run)

    if dry_run:
        print(f"DRY_RUN ativo — {len(image_paths)} imagem(ns) gerada(s); nada publicado.")
        return

    if not config.PLATFORMS:
        print("Nenhuma plataforma configurada (PLATFORMS). Nada publicado.")
        return

    image_urls = _host_images(image_paths)
    if not image_urls:
        print("Aviso: não foi possível hospedar a imagem.", file=sys.stderr)
    is_carousel = len(image_urls) > 1

    errors = []
    for platform in config.PLATFORMS:
        try:
            if platform == "threads":
                if image_urls:
                    post_id = threads.publish_image(image_urls[0], caption)
                else:
                    post_id = threads.publish_text(caption)
            elif platform == "instagram":
                if not image_urls:
                    raise RuntimeError("Instagram requer imagem.")
                post_id = (instagram.publish_carousel(image_urls, caption) if is_carousel
                           else instagram.publish_image(image_urls[0], caption))
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
    entry = {
        "date": datetime.now(brt).isoformat(timespec="minutes"),
        "type": fmt,
        "angle": angle,
        "headline": result.get("main", ""),
    }
    if result.get("_subject"):
        entry["subject"] = result["_subject"]["key"]  # marca o assunto como usado (nunca repetir)
    history.append(entry)


def _build_media(result: dict, asset: dict | None, seed: int, dry_run: bool) -> list[str]:
    """Retorna a lista de imagens do post: 1 card normal, ou vários slides (carrossel)."""
    fmt = result["fmt"]
    tmp = tempfile.gettempdir()
    if fmt == "historia":
        import shutil

        from . import decks, topicphoto

        subj = result.get("_subject") or {}
        query = result.get("image_query") or subj.get("nome", "")
        photo, credit = (None, "")
        try:
            photo, credit = topicphoto.fetch_topic_photo(query)
            print(f"Foto do assunto ('{query}'): {'encontrada' if photo is not None else 'não encontrada'}.")
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: falha ao buscar foto do assunto: {exc}", file=sys.stderr)
        out_dir = "preview_carousel" if dry_run else os.path.join(tmp, "carousel")
        shutil.rmtree(out_dir, ignore_errors=True)
        # Alterna o LAYOUT a cada post (poster / band / frame), com a foto do assunto.
        return decks.build(
            result.get("cover", ""), result.get("slides", []),
            subj.get("hint", ""), config.POST_HANDLE, out_dir, seed, photo=photo, credit=credit,
        )
    out_path = "preview.png" if dry_run else os.path.join(tmp, "post_card.png")
    return [_build_card(result, asset, out_path, seed)]


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

    # Formatos educativos (desenvolvimento do trader).
    subject = result.get("_subject") or {}
    if fmt == "padrao":
        from . import edu

        pat = subject.get("pattern") or {}
        diagram = None
        try:
            diagram = edu.render_pattern(pat, 940, 620, seed=seed) if pat else None
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: não foi possível desenhar o diagrama: {exc}", file=sys.stderr)
        return cards.build_pattern(pat.get("nome", ""), result["explicacao"], diagram, handle, out_path, seed)
    if fmt == "conceito":
        return cards.build_concept(result["titulo"], result["explicacao"], handle, out_path, seed,
                                   badge=subject.get("badge", "APRENDA"))
    if fmt == "dica":
        return cards.build_list(result["title"], result["items"], handle, out_path, seed,
                                badge=subject.get("badge", "APRENDA"))

    # Formatos com foto de IA: foto-reflexão e mercado.
    chart_img = None
    if fmt == "mercado" and asset:
        try:
            from . import chart

            chart_img = chart.render_candles(asset["candles"], asset["label"], asset["change"])
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: não foi possível gerar o gráfico: {exc}", file=sys.stderr)

    # Fundo: foto real (grátis/CC0) primeiro; IA só se houver crédito; senão cena desenhada.
    from . import topicphoto

    q = "stock market charts screen" if fmt == "mercado" else FOTO_QUERIES[seed % len(FOTO_QUERIES)]
    background = None
    try:
        background, _ = topicphoto.fetch_topic_photo(q)
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: falha ao buscar foto de fundo: {exc}", file=sys.stderr)
    if background is None:
        background = imagegen.generate_background("mercado" if fmt == "mercado" else "trader", seed)
        print("Fundo: imagem de IA." if background is not None else "Fundo: cena desenhada.")
    else:
        print(f"Fundo: foto real ('{q}').")
    badge = "mercado" if fmt == "mercado" else "trader"
    return image.build_card(
        result["headline"], badge, handle, out_path, chart_img, seed, background=background
    )


def _host_images(paths: list[str]) -> list[str]:
    """Hospeda 1+ imagens no GitHub (URLs raw) SEM tocar no worktree nem no main.

    Usa plumbing do git (hash-object → mktree → commit-tree) para criar um commit
    isolado com as imagens e faz force-push para o ref `media`. As URLs raw ficam
    pinadas no SHA do commit — públicas e estáveis, sem rebase nem conflito.
    """
    import subprocess
    import time as _time

    paths = [p for p in (paths or []) if p]
    if not paths:
        return []
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        print("Aviso: fora do GitHub Actions — não é possível hospedar a imagem.", file=sys.stderr)
        return []

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
        entries = []
        for i, path in enumerate(paths):
            blob = git(["hash-object", "-w", path]).stdout.strip()
            if not blob:
                return []
            entries.append(f"100644 blob {blob}\timg_{i}.png")
        tree = git(["mktree"], input="".join(e + "\n" for e in entries)).stdout.strip()
        commit = git(["commit-tree", tree, "-m", "cards do post"]).stdout.strip()
        if not commit:
            return []
        for _ in range(4):
            if git(["push", "-f", "origin", f"{commit}:refs/heads/media"]).returncode == 0:
                return [f"https://raw.githubusercontent.com/{repo}/{commit}/img_{i}.png"
                        for i in range(len(paths))]
            _time.sleep(2)
        print("Aviso: falha ao dar push das imagens para o ref media.", file=sys.stderr)
        return []
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: falha ao hospedar imagens no GitHub: {exc}", file=sys.stderr)
        return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera e publica um post sobre trade.")
    parser.add_argument("--type", choices=("trader", *config.ALL_FORMATS), default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(content_type=args.type, dry_run=True if args.dry_run else None)


if __name__ == "__main__":
    main()
