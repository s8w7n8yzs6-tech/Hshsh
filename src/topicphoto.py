"""Foto do ASSUNTO para os carrosséis de notícia.

Usa Pexels (alta qualidade, uso comercial livre) quando PEXELS_API_KEY existir;
senão, cai para o Openverse (sem chave, licenças que permitem uso comercial e
edição), com crédito. Recebe uma busca em inglês (image_query) do tema.
"""
from __future__ import annotations

import io

import requests

from . import config

_UA = {"User-Agent": "HshshBot/1.0 (conteudo editorial de mercado)"}
_MIN = 700  # lado mínimo aceitável


def _open(url: str):
    from PIL import Image

    r = requests.get(url, headers=_UA, timeout=30)
    if r.status_code != 200:
        return None
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    return img if min(img.size) >= _MIN else None


def _pexels(query: str):
    key = getattr(config, "PEXELS_API_KEY", "")
    if not key:
        return None, ""
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "orientation": "portrait", "per_page": 12, "size": "large"},
            headers={"Authorization": key, **_UA}, timeout=25,
        )
        if r.status_code != 200:
            return None, ""
        for p in r.json().get("photos", []):
            src = (p.get("src") or {})
            url = src.get("large2x") or src.get("portrait") or src.get("large")
            img = _open(url) if url else None
            if img is not None:
                return img, ""  # Pexels não exige crédito
    except Exception:  # noqa: BLE001
        pass
    return None, ""


def _openverse(query: str):
    try:
        r = requests.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "page_size": 12, "license": "cc0,pdm,by,by-sa",
                    "orientation": "tall", "mature": "false"},
            headers=_UA, timeout=25,
        )
        if r.status_code != 200:
            return None, ""
        for res in r.json().get("results", []):
            url = res.get("url")
            img = _open(url) if url else None
            if img is not None:
                prov = (res.get("source") or res.get("provider") or "Openverse").title()
                return img, f"foto: {prov} (CC)"
    except Exception:  # noqa: BLE001
        pass
    return None, ""


def fetch_topic_photo(query: str):
    """Retorna (PIL.Image RGB, crédito) da foto do assunto, ou (None, "")."""
    query = (query or "").strip() or "stock market finance"
    img, credit = _pexels(query)
    if img is not None:
        return img, credit
    return _openverse(query)
