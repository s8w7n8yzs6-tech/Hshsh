"""Manchetes de mercado/negócios do Brasil (Google News RSS), ranqueadas por RELEVÂNCIA.

Grátis e sempre atual. Prioriza notícias que chamam a atenção de traders,
empresários e de um público analítico: macro, grandes negócios, movimentos
fortes e temas que fazem pensar — não o factual genérico do dia.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import requests

_UA = {"User-Agent": "Mozilla/5.0 (HshshBot; conteudo educativo de mercado)"}
_FEEDS = [
    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=(Selic%20OR%20Copom%20OR%20juros%20OR%20Fed%20OR%20infla%C3%A7%C3%A3o%20OR%20PIB%20OR%20d%C3%B3lar)%20brasil%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=(IPO%20OR%20aquisi%C3%A7%C3%A3o%20OR%20fus%C3%A3o%20OR%20bilh%C3%B5es%20OR%20lucro%20OR%20preju%C3%ADzo%20OR%20demiss%C3%B5es)%20empresa%20brasil%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=(Ibovespa%20OR%20bolsa%20OR%20a%C3%A7%C3%B5es%20OR%20investidor%20OR%20mercado%20financeiro)%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "https://news.google.com/rss/search?q=(intelig%C3%AAncia%20artificial%20OR%20big%20tech%20OR%20petr%C3%B3leo%20OR%20China%20OR%20economia%20global)%20mercado%20when:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
]
_NOISE = re.compile(
    r"mega-?sena|loteria|quina|lotof|hor[óo]scopo|bbb|novela|futebol|libertadores|"
    r"campeonato|s[ée]rie [a-z]|filme|game|celebridade|resultado sorteado|concurso \d|"
    r"hoje\b.*cota[çc]|veja cota[çc]|confira a cota[çc]",
    re.I,
)
# Sinais de manchete forte (peso positivo).
_HOT = {
    r"bilh(ão|ões)|trilh|milh(ão|ões)|R\$|US\$": 3,
    r"dispara|despenca|salta|desaba|derrete|afunda|recorde|explode|dispar|bater|máxima|mínima": 3,
    r"selic|copom|juros|fed|infla[çc]|pib|d[óo]lar|c[âa]mbio|fiscal|reforma|imposto|tarifa": 2,
    r"ipo|aquisi[çc]|fus[ãa]o|lucro|preju[íi]zo|demiss|falência|recupera[çc]ão judicial|balan[çc]o": 2,
    r"intelig[êe]ncia artificial|\bia\b|big tech|nvidia|tesla|petr[óo]leo|ouro|bitcoin|china|eua|trump|guerra": 2,
    r"por que|entenda|o que muda|analistas|alerta|risco|an[áa]lise|estrat[ée]gia": 1,
}
_COLD = re.compile(r"abre (em|no)|fecha (em|no)|opera em|no radar\b|ao vivo|minuto a minuto", re.I)


def _clean(title: str) -> str:
    return re.sub(r"\s+-\s+[^-]+$", "", title or "").strip()


def _slug(title: str) -> str:
    import unicodedata

    t = unicodedata.normalize("NFKD", title.lower()).encode("ascii", "ignore").decode()
    return "-".join(re.findall(r"[a-z0-9]+", t)[:6]) or "x"


def _score(title: str) -> int:
    s = 0
    for pat, w in _HOT.items():
        if re.search(pat, title, re.I):
            s += w
    if _COLD.search(title):
        s -= 2
    if len(title) >= 55:
        s += 1
    return s


def fetch_headlines(limit: int = 20) -> list[dict]:
    """Manchetes recentes ranqueadas: [{title, source, slug, score}] (mais forte primeiro)."""
    seen: set = set()
    items: list[dict] = []
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
            if not title or len(title) < 26 or _NOISE.search(title):
                continue
            slug = _slug(title)
            if slug in seen:
                continue
            seen.add(slug)
            src = it.find("source")
            items.append({
                "title": title,
                "source": (src.text if src is not None else "").strip(),
                "slug": slug,
                "score": _score(title),
            })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items[:limit]
