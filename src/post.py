"""Orquestrador: gera 1 post e publica nas plataformas configuradas.

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

    snapshot = market.get_market_snapshot() if content_type == "mercado" else None
    caption = generate.generate_post(content_type, snapshot)

    print(f"[{content_type}] Post gerado:\n{caption}\n")

    if dry_run:
        print("DRY_RUN ativo — nada foi publicado.")
        return

    if not config.PLATFORMS:
        print("Nenhuma plataforma configurada (PLATFORMS). Nada publicado.")
        return

    # Gera a imagem só se o Instagram estiver entre os destinos.
    image_url = None
    if "instagram" in config.PLATFORMS or "threads" in config.PLATFORMS:
        image_url = _maybe_upload_image(caption)

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
                    raise RuntimeError("Instagram requer imagem, mas o upload falhou.")
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


def _maybe_upload_image(caption: str) -> str | None:
    """Gera e hospeda a imagem; retorna a URL ou None se não for possível."""
    from . import image, image_host

    if "instagram" in config.PLATFORMS and not config.IMGBB_API_KEY:
        # Instagram precisa de imagem; sem host não dá para prosseguir com ela.
        print("Aviso: IMGBB_API_KEY ausente — Instagram não poderá publicar imagem.")
    if not config.IMGBB_API_KEY:
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            path = tmp.name
        image.render_caption_image(caption, path)
        url = image_host.upload_image(path)
        os.unlink(path)
        return url
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: não foi possível gerar/hospedar imagem: {exc}", file=sys.stderr)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera e publica um post sobre trade.")
    parser.add_argument("--type", choices=config.CONTENT_TYPES, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(content_type=args.type, dry_run=True if args.dry_run else None)


if __name__ == "__main__":
    main()
