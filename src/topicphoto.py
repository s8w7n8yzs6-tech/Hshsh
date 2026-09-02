"""Foto do ASSUNTO para os carrosséis de notícia — sem precisar de chave.

Prioriza fontes de STOCK PHOTO em CC0 dentro do Openverse (Rawpixel/StockSnap):
qualidade profissional, uso comercial livre e sem exigência de crédito. Depois
tenta o Openverse geral (licenças que permitem uso comercial + edição, com
crédito) e, por último, a Wikipédia. Pexels é usado só se houver PEXELS_API_KEY.
"""
from __future__ import annotations

import io
import re

import requests

from . import config

_UA = {"User-Agent": "HshshBot/1.0 (conteudo editorial de mercado)"}
_API = "https://api.openverse.org/v1/images/"
# Descarta clipart/vetor/mockup — queremos FOTO.
_BAD = re.compile(
    # não-foto
    r"clipart|illustration|vector|icon|psd|mockup|collage|border|frame|sticker|"
    r"pattern|drawing|logo|template|transparent|"
    # material antigo/arquivo (o acervo CC0 tem muita foto histórica)
    r"vintage|antique|retro|archive|museum|painting|engraving|postcard|lithograph|"
    r"original image from|public domain|18\d\d|19[0-7]\d",
    re.I,
)
_MIN_LONG = 800   # lado maior mínimo
_MIN_SHORT = 560  # lado menor mínimo


def _download(url: str):
    from PIL import Image

    try:
        r = requests.get(url, headers=_UA, timeout=30)
        if r.status_code != 200:
            return None
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
    except Exception:  # noqa: BLE001
        return None
    w, h = img.size
    if max(w, h) < _MIN_LONG or min(w, h) < _MIN_SHORT:
        return None
    return img


def _pick(results, want_tall: bool):
    """Baixa e devolve a melhor foto da lista (prefere alta resolução e retrato)."""
    best, best_score = None, -1
    for res in results[:10]:
        if _BAD.search(res.get("title") or ""):
            continue
        img = _download(res.get("url") or "")
        if img is None:
            continue
        w, h = img.size
        score = (w * h) / 1_000_000.0
        if want_tall:
            score += 2.5 * (h / w)
        if score > best_score:
            best, best_score = (img, res), score
        if best_score > 4:  # bom o bastante
            break
    return best


def _openverse(query: str, sources: str | None, licenses: str | None, tall: bool):
    params = {"q": query, "page_size": 12, "mature": "false", "size": "large"}
    if sources:
        params["source"] = sources
    if licenses:
        params["license"] = licenses
    if tall:
        params["aspect_ratio"] = "tall"
    try:
        r = requests.get(_API, params=params, headers=_UA, timeout=25)
        if r.status_code != 200:
            return None
        return r.json().get("results", []) or None
    except Exception:  # noqa: BLE001
        return None


def _pexels(query: str):
    key = getattr(config, "PEXELS_API_KEY", "")
    if not key:
        return None, ""
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            params={"query": query, "orientation": "portrait", "per_page": 10, "size": "large"},
            headers={"Authorization": key, **_UA}, timeout=25,
        )
        if r.status_code == 200:
            for p in r.json().get("photos", []):
                src = p.get("src") or {}
                img = _download(src.get("large2x") or src.get("portrait") or src.get("large") or "")
                if img is not None:
                    return img, ""
    except Exception:  # noqa: BLE001
        pass
    return None, ""


def _wikipedia(query: str):
    try:
        from . import photos

        img, credit = photos.fetch_person_photo(query)
        return img, credit
    except Exception:  # noqa: BLE001
        return None, ""


def fetch_topic_photo(query: str):
    """Retorna (PIL.Image RGB, crédito) da foto do assunto, ou (None, "")."""
    q = (query or "").strip() or "stock market finance"
    short = " ".join(q.split()[:2])

    img, credit = _pexels(q)
    if img is not None:
        return img, credit

    # 1) Stock CC0 (sem exigência de crédito): retrato primeiro, depois qualquer.
    for qq in (q, short):
        for tall in (True, False):
            res = _openverse(qq, "rawpixel,stocksnap", "cc0,pdm", tall)
            if res:
                got = _pick(res, want_tall=tall)
                if got:
                    return got[0], ""

    # 2) Openverse geral (uso comercial + edição) — com crédito.
    for qq in (q, short):
        res = _openverse(qq, None, "cc0,pdm,by,by-sa", False)
        if res:
            got = _pick(res, want_tall=True)
            if got:
                prov = (got[1].get("source") or "Openverse").title()
                lic = (got[1].get("license") or "").lower()
                return got[0], "" if lic in ("cc0", "pdm") else f"foto: {prov} (CC)"

    # 3) Último recurso: Wikipédia/Commons.
    return _wikipedia(q)
