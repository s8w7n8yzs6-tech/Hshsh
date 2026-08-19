"""Busca a foto de uma pessoa na Wikipédia/Wikimedia Commons (uso livre, com crédito).

Usa a REST API da Wikipédia (não a action API, que é limitada por IP). Nunca gera
foto falsa de pessoa real — apenas reutiliza imagens de licença livre, creditando.
"""
from __future__ import annotations

import io
import urllib.parse

import requests

_UA = {"User-Agent": "HshshInstagramBot/1.0 (conteudo educativo sobre mercado)"}


def _search_title(nome: str, lang: str) -> str | None:
    r = requests.get(
        f"https://{lang}.wikipedia.org/w/rest.php/v1/search/title",
        params={"q": nome, "limit": 1}, headers=_UA, timeout=20,
    )
    if r.status_code != 200:
        return None
    pages = r.json().get("pages", [])
    return pages[0]["title"] if pages else None


def _summary_image(title: str, lang: str) -> str | None:
    t = urllib.parse.quote(title.replace(" ", "_"))
    r = requests.get(
        f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{t}", headers=_UA, timeout=20,
    )
    if r.status_code != 200:
        return None
    d = r.json()
    src = (d.get("originalimage") or {}).get("source") or (d.get("thumbnail") or {}).get("source")
    if src and src.lower().split("?")[0].endswith(".svg"):
        return None
    return src


def fetch_person_photo(nome: str):
    """Retorna (PIL.Image RGB, crédito) da foto da pessoa, ou (None, "") se não achar."""
    from PIL import Image

    for lang in ("pt", "en"):
        try:
            title = _search_title(nome, lang) or nome
            src = _summary_image(title, lang)
            if not src:
                continue
            b = requests.get(src, headers=_UA, timeout=30)
            if b.status_code != 200:
                continue
            img = Image.open(io.BytesIO(b.content)).convert("RGB")
            if min(img.size) < 200:  # muito pequena, provavelmente ícone
                continue
            return img, "foto: Wikimedia Commons"
        except Exception:  # noqa: BLE001 — sem foto, cai para a capa tipográfica
            continue
    return None, ""
