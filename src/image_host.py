"""Hospeda uma imagem publicamente via imgbb e retorna a URL.

O Instagram Graph API exige uma URL de imagem publicamente acessível — não
aceita upload direto de binário. Usamos o imgbb (grátis) para isso.
"""
from __future__ import annotations

import base64

import requests

from . import config

_URL = "https://api.imgbb.com/1/upload"


def upload_image(path: str, timeout: int = 30) -> str:
    """Envia a imagem em `path` ao imgbb e retorna a URL pública. Levanta em falha."""
    if not config.IMGBB_API_KEY:
        raise RuntimeError(
            "IMGBB_API_KEY não configurada — necessária para publicar imagem no Instagram."
        )
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    resp = requests.post(
        _URL,
        data={"key": config.IMGBB_API_KEY, "image": encoded},
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["url"]
