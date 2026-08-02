"""Publicação no Instagram via Instagram API (login do Instagram, graph.instagram.com).

Fluxo em 2 passos: cria o contêiner de mídia e depois publica.
O Instagram exige mídia (imagem) com URL pública — não há post só de texto.
"""
from __future__ import annotations

import requests

from .. import config

_BASE = "https://graph.instagram.com/v21.0"


def publish_image(image_url: str, caption: str, timeout: int = 30) -> str:
    """Publica uma imagem com legenda no Instagram e retorna o ID da mídia."""
    if not (config.INSTAGRAM_USER_ID and config.INSTAGRAM_ACCESS_TOKEN):
        raise RuntimeError(
            "Credenciais do Instagram ausentes (INSTAGRAM_USER_ID / INSTAGRAM_ACCESS_TOKEN)."
        )

    create = requests.post(
        f"{_BASE}/{config.INSTAGRAM_USER_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": config.INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=timeout,
    )
    create.raise_for_status()
    creation_id = create.json()["id"]

    publish = requests.post(
        f"{_BASE}/{config.INSTAGRAM_USER_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": config.INSTAGRAM_ACCESS_TOKEN},
        timeout=timeout,
    )
    publish.raise_for_status()
    return publish.json()["id"]
