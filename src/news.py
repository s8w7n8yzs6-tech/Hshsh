"""Fonte de manchetes: assuntos em alta no mercado/negócios do Brasil (Google News RSS).

Grátis e sempre atual. Retorna manchetes limpas com a fonte, para virar carrossel.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import requests

_UA = {"User-Agent": "Mozilla/5.0 (HshshBot; conteudo educativo de mercado)"}
_FEEDS = [
    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=mercado%20financeiro%20OR%20bolsa%20OR%20economia%20brasil%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=empresas%20OR%20investimentos%20OR%20juros%20OR%20d%C3%B3lar%20brasil%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
]
# Ruído a descartar (loteria, esportes, entretenimento, etc.).
_NOISE = re.compile(
    r"mega-?sena|loteria|quina|lotof|hor[óo]scopo|bbb|novela|futebol|libertadores|"
    r"campeonato|s[ée]rie|filme|game|celebridade|resultado sorteado|concurso \d",
    re.I,
)


def _clean(title: str) -> str:
    return re.sub(r"\s+-\s+[^-]+$", "", title or "").strip()


def _slug(title: str) -> str:
    import unicodedata

    t = unicodedata.normalize("NFKD", title.lower()).encode("ascii", "ignore").decode()
    return "-".join(re.findall(r"[a-z0-9]+", t)[:6]) or "x"


def fetch_headlines(limit: int = 25) -> list[dict]:
    """Manchetes recentes de mercado/negócios do Brasil: [{title, source, slug}]."""
    seen: set = set()
    out: list[dict] = []
    for url in _FEEDS:
        try:
            r = requests.get(url, headers=_UA, timeout=25)
            if r.status_code != 200:
                continue
            root = ET.fromstring(r.content)
        except Exception:  # noqa: BLE001
            continue
        for it in root.findall(".//item"):
            title = _clean(it.findtext("title") or "")
            if not title or len(title) < 24 or _NOISE.search(title):
                continue
            src = it.find("source")
            source = (src.text if src is not None else "").strip()
            slug = _slug(title)
            if slug in seen:
                continue
            seen.add(slug)
            out.append({"title": title, "source": source, "slug": slug})
            if len(out) >= limit:
                return out
    return out
