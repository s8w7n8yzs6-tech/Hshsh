"""Publicação no Threads via Graph API (fluxo em 2 passos: criar + publicar)."""
from __future__ import annotations

import requests

from .. import config

_BASE = "https://graph.threads.net/v1.0"


def _create_container(payload: dict, timeout: int) -> str:
    resp = requests.post(f"{_BASE}/{config.THREADS_USER_ID}/threads", data=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["id"]


def _publish(creation_id: str, timeout: int) -> str:
    resp = requests.post(
        f"{_BASE}/{config.THREADS_USER_ID}/threads_publish",
        data={"creation_id": creation_id, "access_token": config.THREADS_ACCESS_TOKEN},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def publish_text(text: str, timeout: int = 30) -> str:
    """Publica um post de texto no Threads e retorna o ID do post."""
    if not (config.THREADS_USER_ID and config.THREADS_ACCESS_TOKEN):
        raise RuntimeError("Credenciais do Threads ausentes (THREADS_USER_ID / THREADS_ACCESS_TOKEN).")
    creation_id = _create_container(
        {"media_type": "TEXT", "text": text, "access_token": config.THREADS_ACCESS_TOKEN},
        timeout,
    )
    return _publish(creation_id, timeout)


def publish_image(image_url: str, text: str, timeout: int = 30) -> str:
    """Publica um post com imagem no Threads e retorna o ID do post."""
    if not (config.THREADS_USER_ID and config.THREADS_ACCESS_TOKEN):
        raise RuntimeError("Credenciais do Threads ausentes (THREADS_USER_ID / THREADS_ACCESS_TOKEN).")
    creation_id = _create_container(
        {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
            "access_token": config.THREADS_ACCESS_TOKEN,
        },
        timeout,
    )
    return _publish(creation_id, timeout)
