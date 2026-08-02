"""Publicação no Instagram via Instagram API (login do Instagram, graph.instagram.com).

Fluxo em 3 passos: cria o contêiner de mídia, espera ficar pronto (FINISHED) e
publica. O Instagram exige mídia (imagem) com URL pública — não há post só de texto.
"""
from __future__ import annotations

import time

import requests

from .. import config

_BASE = "https://graph.instagram.com/v21.0"


def _post(url: str, data: dict, timeout: int) -> dict:
    r = requests.post(url, data=data, timeout=timeout)
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} em {url.split('/')[-1]}: {r.text[:400]}")
    return r.json()


def _wait_ready(creation_id: str, timeout: int, attempts: int = 12, delay: int = 3) -> None:
    """Aguarda o contêiner de mídia terminar o processamento antes de publicar."""
    url = f"{_BASE}/{creation_id}"
    for _ in range(attempts):
        r = requests.get(
            url,
            params={"fields": "status_code,status", "access_token": config.INSTAGRAM_ACCESS_TOKEN},
            timeout=timeout,
        )
        code = r.json().get("status_code") if r.status_code < 400 else None
        if code == "FINISHED":
            return
        if code == "ERROR":
            raise RuntimeError(f"contêiner de mídia falhou: {r.text[:400]}")
        time.sleep(delay)
    raise RuntimeError("contêiner de mídia não ficou pronto a tempo (timeout)")


def publish_image(image_url: str, caption: str, timeout: int = 30) -> str:
    """Publica uma imagem com legenda no Instagram e retorna o ID da mídia."""
    if not (config.INSTAGRAM_USER_ID and config.INSTAGRAM_ACCESS_TOKEN):
        raise RuntimeError(
            "Credenciais do Instagram ausentes (INSTAGRAM_USER_ID / INSTAGRAM_ACCESS_TOKEN)."
        )

    creation = _post(
        f"{_BASE}/{config.INSTAGRAM_USER_ID}/media",
        {
            "image_url": image_url,
            "caption": caption,
            "access_token": config.INSTAGRAM_ACCESS_TOKEN,
        },
        timeout,
    )
    creation_id = creation["id"]

    _wait_ready(creation_id, timeout)

    published = _post(
        f"{_BASE}/{config.INSTAGRAM_USER_ID}/media_publish",
        {"creation_id": creation_id, "access_token": config.INSTAGRAM_ACCESS_TOKEN},
        timeout,
    )
    return published["id"]
