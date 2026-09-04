"""Manchetes de mercado/economia/negócios (Google Notícias RSS), ranqueadas por RELEVÂNCIA.

Grátis e sempre atual. São 10 fontes temáticas (macro, empresas, bolsa, energia,
varejo, tecnologia, cripto/renda fixa, Wall Street...) para garantir volume e
VARIEDADE suficientes para 20 carrosséis por dia sem repetir assunto.

Cada manchete vem com o `topic` (a editoria de onde saiu), usado como tarja do
carrossel, e com `keys` — as palavras fortes do título, que permitem descartar
manchetes que contam a MESMA história com outras palavras.
"""
from __future__ import annotations

import re
import unicodedata
import xml.etree.ElementTree as ET

import requests

_UA = {"User-Agent": "Mozilla/5.0 (HshshBot; conteudo educativo de mercado)"}
_MAX_POOL = 120  # teto de manchetes distintas guardadas por execução


def _feed(query: str) -> str:
    from urllib.parse import quote

    return ("https://news.google.com/rss/search?q=" + quote(query)
            + "&hl=pt-BR&gl=BR&ceid=BR:pt-419")


# (editoria, url). A editoria vira a tarja do carrossel — dá cara de jornal.
_FEEDS: list[tuple[str, str]] = [
    ("Economia",
     "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-BR&gl=BR&ceid=BR:pt-419"),
    ("Macro & Juros",
     _feed("(Selic OR Copom OR juros OR Fed OR inflação OR IPCA OR PIB OR dólar OR câmbio) brasil when:7d")),
    ("Empresas",
     _feed("(IPO OR aquisição OR fusão OR bilhões OR lucro OR prejuízo OR demissões OR balanço) empresa brasil when:7d")),
    ("Bolsa & Investimentos",
     _feed("(Ibovespa OR bolsa OR ações OR investidor OR mercado financeiro OR B3) when:7d")),
    ("Global & Tecnologia",
     _feed("(inteligência artificial OR big tech OR Nvidia OR OpenAI OR economia global OR China) mercado when:7d")),
    ("Energia & Commodities",
     _feed("(Petrobras OR petróleo OR Vale OR minério OR energia OR agro OR safra OR commodities) preço when:7d")),
    ("Varejo & Consumo",
     _feed("(varejo OR consumo OR e-commerce OR emprego OR salário OR crédito OR endividamento) brasileiro when:7d")),
    ("Bancos & Fintech",
     _feed("(banco OR fintech OR Nubank OR Pix OR crédito OR seguros OR open finance) brasil when:7d")),
    ("Cripto & Renda Fixa",
     _feed("(bitcoin OR criptomoeda OR ETF OR tesouro direto OR renda fixa OR CDI OR fundos) investimento when:7d")),
    ("Wall Street",
     _feed("(Wall Street OR Nasdaq OR S&P 500 OR Fed OR treasuries OR recessão) mercado when:7d")),
]

_NOISE = re.compile(
    r"mega-?sena|loteria|quina|lotof|hor[óo]scopo|bbb|novela|futebol|libertadores|"
    r"campeonato|s[ée]rie [a-z]|filme|game|celebridade|resultado sorteado|concurso \d|"
    r"hoje\b.*cota[çc]|veja cota[çc]|confira a cota[çc]|ao vivo|minuto a minuto|"
    r"veja as? fotos|patroc[íi]nio|publieditorial",
    re.I,
)
# Sinais de manchete forte (peso positivo).
_HOT = {
    r"bilh(ão|ões)|trilh|milh(ão|ões)|R\$|US\$|%": 3,
    r"dispara|despenca|salta|desaba|derrete|afunda|recorde|explode|dispar|bater|máxima|mínima": 3,
    r"selic|copom|juros|fed|infla[çc]|pib|d[óo]lar|c[âa]mbio|fiscal|reforma|imposto|tarifa": 2,
    r"ipo|aquisi[çc]|fus[ãa]o|lucro|preju[íi]zo|demiss|falência|recupera[çc]ão judicial|balan[çc]o": 2,
    r"intelig[êe]ncia artificial|\bia\b|big tech|nvidia|tesla|petr[óo]leo|ouro|bitcoin|china|eua|trump|guerra": 2,
    r"por que|entenda|o que muda|analistas|alerta|risco|an[áa]lise|estrat[ée]gia|efeito|impacto": 1,
}
_COLD = re.compile(r"abre (em|no)|fecha (em|no)|opera em|no radar\b|agenda do dia|resumo do dia", re.I)

# Palavras sem peso para comparar duas manchetes (não identificam a história).
_WEAK = {
    "para", "como", "mais", "menos", "sobre", "apos", "após", "pelo", "pela", "com",
    "sem", "dos", "das", "nos", "nas", "que", "uma", "seu", "sua", "ser", "vai",
    "diz", "tem", "ate", "até", "por", "entenda", "veja", "saiba", "brasil",
    "brasileiro", "brasileira", "mercado", "novo", "nova", "ano", "anos", "hoje",
    "semana", "governo", "milhoes", "bilhoes", "empresa", "empresas",
}


def _ascii(text: str) -> str:
    return unicodedata.normalize("NFKD", (text or "").lower()).encode("ascii", "ignore").decode()


def _clean(title: str) -> str:
    return re.sub(r"\s+-\s+[^-]+$", "", title or "").strip()


def _slug(title: str) -> str:
    return "-".join(re.findall(r"[a-z0-9]+", _ascii(title))[:6]) or "x"


def keywords(text: str) -> set:
    """Palavras fortes de um título/slug — a 'impressão digital' da história."""
    return {w for w in re.findall(r"[a-z0-9]{4,}", _ascii(text)) if w not in _WEAK}


# Tipos de FATO. Duas manchetes que citam o mesmo protagonista E são do mesmo
# tipo de fato contam a mesma história, ainda que com títulos bem diferentes
# ("Nvidia faz aquisição bilionária" e "a startup que a Nvidia vai comprar").
_EVENTOS = (
    r"aquisi|compr[ao]|adquir|fus[ãa]o|merger|incorpora",
    r"\bipo\b|abertura de capital|estreia na bolsa",
    r"lucro|preju[íi]zo|balan[çc]o|resultado|receita",
    r"demiss|corte de vagas|layoff|fecha unidade",
    r"fal[êe]ncia|recupera[çc][ãa]o judicial|calote",
    r"juros|selic|copom|taxa b[áa]sica",
)


def _evento(text: str) -> str:
    import re as _re

    t = _ascii(text)
    for i, pat in enumerate(_EVENTOS):
        if _re.search(_ascii(pat), t):
            return str(i)
    return ""


def same_story(a: str, b: str, min_overlap: int = 2) -> bool:
    """Duas manchetes falam do MESMO fato? (compara as palavras fortes)."""
    ka, kb = keywords(a), keywords(b)
    if not ka or not kb:
        return False
    comum = ka & kb
    if len(comum) >= min_overlap:
        return True
    # Mesmo PROTAGONISTA + mesmo tipo de fato (ex.: Nvidia + aquisição). A palavra
    # em comum precisa ser o protagonista, não o próprio evento: senão duas
    # decisões de juros diferentes (Fed e BC do Canadá) virariam a mesma notícia.
    ev = _evento(a)
    if not ev or ev != _evento(b):
        return False
    return bool({w for w in comum if not _evento(w)})


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


_CACHE: list[dict] = []  # as manchetes são buscadas UMA vez por execução


def fetch_headlines(limit: int = 60) -> list[dict]:
    """Manchetes recentes ranqueadas: [{title, source, topic, slug, keys, score}].

    Já vem sem repetição de HISTÓRIA: quando dois veículos publicam o mesmo fato,
    fica só a versão de manchete mais forte. O resultado fica em cache durante a
    execução (um disparo pode publicar vários posts sem rebuscar os 10 feeds).
    """
    if _CACHE:
        return _CACHE[:limit]

    seen_slug: set = set()
    items: list[dict] = []
    for topic, url in _FEEDS:
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
            if slug in seen_slug:
                continue
            seen_slug.add(slug)
            src = it.find("source")
            items.append({
                "title": title,
                "source": (src.text if src is not None else "").strip(),
                "topic": topic,
                "slug": slug,
                "keys": sorted(keywords(title)),
                "score": _score(title),
            })

    items.sort(key=lambda x: x["score"], reverse=True)

    # Colapsa manchetes diferentes sobre o MESMO fato (fica a mais forte).
    unique: list[dict] = []
    for it in items:
        if any(same_story(it["title"], u["title"]) for u in unique):
            continue
        unique.append(it)
        if len(unique) >= _MAX_POOL:
            break
    _CACHE[:] = unique
    return unique[:limit]
