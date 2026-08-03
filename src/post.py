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

from . import config, generate, market
from .publishers import instagram, threads


def _current_slot() -> int:
    """Índice do horário agendado (SCHEDULE_BRT) mais próximo de agora (Brasília)."""
    brt = timezone(timedelta(hours=config.BRT_OFFSET_HOURS))
    now = datetime.now(brt)
    minutes = now.hour * 60 + now.minute
    diffs = [abs(minutes - (h * 60 + m)) for h, m in config.SCHEDULE_BRT]
    return diffs.index(min(diffs))


def plan_post(content_type: str | None) -> tuple[str, str | None]:
    """Decide (tipo, ativo). 2 slots/dia são de mercado (ouro/Nasdaq); o resto, trader."""
    ct = content_type or config.POST_TYPE
    if ct == "mercado":
        return "mercado", random.choice(list(market.MARKET_ASSETS))
    if ct:  # tipo fixo (ex.: "trader")
        return ct, None

    slot = _current_slot()
    if slot == config.GOLD_SLOT_INDEX:
        return "mercado", "ouro"
    if slot == config.NASDAQ_SLOT_INDEX:
        return "mercado", "nasdaq"
    return "trader", None


def _variety(content_type: str) -> tuple[str | None, str | None]:
    """Escolhe (ângulo, estilo) para dar variedade e evitar posts repetidos."""
    if content_type == "mercado":
        return random.choice(config.MARKET_ANGLES), None
    if content_type == "trader":
        brt = timezone(timedelta(hours=config.BRT_OFFSET_HOURS))
        day = datetime.now(brt).timetuple().tm_yday
        # (slot + dia): não repete no mesmo dia e a rotação muda a cada dia.
        angle = config.TRADER_ANGLES[(_current_slot() + day) % len(config.TRADER_ANGLES)]
        return angle, random.choice(config.TRADER_FORMATS)
    return None, None


def run(content_type: str | None = None, dry_run: bool | None = None) -> None:
    content_type, asset_key = plan_post(content_type)
    dry_run = config.DRY_RUN if dry_run is None else dry_run

    asset = None
    snapshot = None
    if content_type == "mercado":
        asset = market.fetch_asset(asset_key)
        if not asset:  # se falhar o ativo, cai para conteúdo de trader
            content_type = "trader"
        else:
            snapshot = market.asset_snapshot(asset)

    angle, style = _variety(content_type)
    result = generate.generate_post(content_type, snapshot, angle=angle, style=style)
    used_type = result["type"]
    caption = result["caption"]
    headline = result["headline"]

    print(f"[{used_type}] headline: {headline}")
    print(f"legenda:\n{caption}\n")

    # Sempre gera o card visual.
    out_path = "preview.png" if dry_run else os.path.join(tempfile.gettempdir(), "post_card.png")
    image_path = _build_card(headline, used_type, asset, out_path)

    if dry_run:
        print(f"DRY_RUN ativo — card salvo em {image_path}; nada publicado.")
        return

    if not config.PLATFORMS:
        print("Nenhuma plataforma configurada (PLATFORMS). Nada publicado.")
        return

    image_url = _host_image(image_path)
    if image_url is None:
        print("Aviso: sem IMGBB_API_KEY — publicando sem imagem onde possível.", file=sys.stderr)

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


def _build_card(headline: str, content_type: str, asset: dict | None, out_path: str) -> str:
    from . import image

    chart_img = None
    if content_type == "mercado" and asset:
        try:
            from . import chart

            chart_img = chart.render_candles(asset["candles"], asset["label"], asset["change"])
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: não foi possível gerar o gráfico: {exc}", file=sys.stderr)
    return image.build_card(headline, content_type, config.POST_HANDLE, out_path, chart_img)


def _host_image(path: str) -> str | None:
    if not config.IMGBB_API_KEY:
        return None
    try:
        from . import image_host

        return image_host.upload_image(path)
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: não foi possível hospedar a imagem: {exc}", file=sys.stderr)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera e publica um post sobre trade.")
    parser.add_argument("--type", choices=config.CONTENT_TYPES, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(content_type=args.type, dry_run=True if args.dry_run else None)


if __name__ == "__main__":
    main()
