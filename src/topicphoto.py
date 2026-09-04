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
    r"original image from|public domain|18\d\d|19[0-7]\d|"
    # negativos/escaneados de acervo (chegam como foto, mas parecem filme velho)
    r"negative|film strip|safety film|agfa|kodak|glass plate|daguerre|"
    r"scanned|photographic print|black.and.white|black & white|monochrome|b&w",
    re.I,
)
_MIN_LONG = 800   # lado maior mínimo
_MIN_SHORT = 560  # lado menor mínimo
_MIN_SAT = 10     # saturação média mínima: abaixo disso é P&B/negativo de acervo


def _saturation(img) -> float:
    """Saturação média (0-255). Fotos modernas têm cor; escaneados antigos, não."""
    try:
        small = img.convert("HSV").resize((64, 64))
        px = small.split()[1].getdata()
        return sum(px) / len(px)
    except Exception:  # noqa: BLE001
        return 255.0


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
    if _saturation(img) < _MIN_SAT:
        return None  # imagem sem cor (P&B/negativo antigo) — não serve de capa
    return img


_STOP = {"the", "and", "with", "from", "into", "over", "photo", "image"}


def _tokens(query: str) -> list[str]:
    return [w for w in re.findall(r"[a-z]{4,}", query.lower()) if w not in _STOP]


def _relevant(title: str, toks: list[str]) -> bool:
    """Título precisa citar alguma palavra da busca (evita foto sem relação)."""
    t = (title or "").lower()
    return any(w in t for w in toks) if toks else True


def _pick(results, want_tall: bool, toks: list[str] | None = None):
    """Baixa e devolve a melhor foto da lista (prefere alta resolução e retrato)."""
    best, best_score = None, -1
    for res in results[:12]:
        title = res.get("title") or ""
        if _BAD.search(title):
            continue
        if toks and not _relevant(title, toks):
            continue
        img = _download(res.get("url") or "")
        if img is None:
            continue
        w, h = img.size
        score = (w * h) / 1_000_000.0
        score += min(2.0, _saturation(img) / 60.0)  # foto com cor chama mais atenção
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

    # 1) Stock CC0 (sem crédito): StockSnap (moderno) antes do Rawpixel (mais arquivo).
    toks = _tokens(q)
    for src in ("stocksnap", "rawpixel,stocksnap"):
        for qq in (q, short):
            for tall in (True, False):
                res = _openverse(qq, src, "cc0,pdm", tall)
                if res:
                    got = _pick(res, want_tall=tall, toks=toks)
                    if got:
                        return got[0], ""

    # 2) Openverse geral (uso comercial + edição) — com crédito.
    for qq in (q, short):
        res = _openverse(qq, None, "cc0,pdm,by,by-sa", False)
        if res:
            got = _pick(res, want_tall=True, toks=toks)
            if got:
                prov = (got[1].get("source") or "Openverse").title()
                lic = (got[1].get("license") or "").lower()
                return got[0], "" if lic in ("cc0", "pdm") else f"foto: {prov} (CC)"

    # 3) Último recurso: Wikipédia/Commons.
    return _wikipedia(q)
