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

from . import config, generate, market
from .publishers import instagram, threads


def choose_type() -> str:
    if config.POST_TYPE:
        return config.POST_TYPE
    return random.choices(config.CONTENT_TYPES, weights=config.CONTENT_WEIGHTS, k=1)[0]


def run(content_type: str | None = None, dry_run: bool | None = None) -> None:
    content_type = content_type or choose_type()
    dry_run = config.DRY_RUN if dry_run is None else dry_run

    # Posts de mercado: foca em UM ativo (ouro ou Nasdaq), alternado, com candles 30min.
    asset = None
    snapshot = None
    if content_type == "mercado":
        for key in random.sample(list(market.MARKET_ASSETS), k=len(market.MARKET_ASSETS)):
            asset = market.fetch_asset(key)  # tenta o primeiro; se falhar, o outro
            if asset:
                break
        snapshot = market.asset_snapshot(asset) if asset else None

    result = generate.generate_post(content_type, snapshot)
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
