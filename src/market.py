"""Dados de mercado reais para Ouro (XAU/USD) e Nasdaq 100, via Yahoo Finance.

Fornece candles OHLC de 30 min (para o gráfico de candlestick) e preço/variação
no dia. Endpoint público, sem chave. Números reais, não inventados.
"""
from __future__ import annotations

import requests

# chave interna -> (símbolo Yahoo, rótulo, sigla). GC=F (ouro futuro) ~ XAU/USD spot.
_ASSETS = {
    "ouro": {"symbol": "GC=F", "label": "Ouro (XAU/USD)", "short": "XAU/USD"},
    "nasdaq": {"symbol": "^NDX", "label": "Nasdaq 100", "short": "NASDAQ"},
}
MARKET_ASSETS = ("ouro", "nasdaq")

_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
_HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_asset(key: str, interval: str = "30m", rng: str = "5d", count: int = 48,
                timeout: int = 20) -> dict | None:
    """Retorna dados de um ativo com os últimos `count` candles OHLC, ou None em falha.

    {"key","label","short","price","change","interval","candles":[{o,h,l,c}, ...]}
    """
    asset = _ASSETS.get(key)
    if not asset:
        return None
    try:
        resp = requests.get(
            _URL.format(symbol=asset["symbol"]),
            params={"range": rng, "interval": interval},
            headers=_HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        ts = result["timestamp"]
        q = result["indicators"]["quote"][0]
        o, h, l, c = q["open"], q["high"], q["low"], q["close"]
        meta = result["meta"]
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return None

    candles = [
        {"o": o[i], "h": h[i], "l": l[i], "c": c[i]}
        for i in range(len(ts))
        if None not in (o[i], h[i], l[i], c[i])
    ]
    if len(candles) < 5:
        return None
    candles = candles[-count:]

    price = meta.get("regularMarketPrice") or candles[-1]["c"]
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    change = ((price - prev) / prev * 100) if prev else 0.0

    return {
        "key": key,
        "label": asset["label"],
        "short": asset["short"],
        "price": float(price),
        "change": float(change),
        "interval": interval,
        "candles": candles,
    }


def asset_snapshot(a: dict) -> str:
    """Resumo factual de um ativo para o modelo (contexto do post de mercado)."""
    highs = [c["h"] for c in a["candles"]]
    lows = [c["l"] for c in a["candles"]]
    return (
        f"Ativo: {a['label']} (gráfico de candlestick, candles de 30 min)\n"
        f"Preço atual: {a['price']:,.2f}\n"
        f"Variação no dia: {a['change']:+.2f}%\n"
        f"Máxima recente: {max(highs):,.2f} | Mínima recente: {min(lows):,.2f}"
    )


def get_market_data(timeout: int = 15) -> list[dict] | None:
    """Resumo de preço/variação dos dois ativos (usado no verificador)."""
    out = []
    for key in MARKET_ASSETS:
        a = fetch_asset(key, count=2, timeout=timeout)
        if a:
            out.append({"label": a["label"], "short": a["short"], "price": a["price"], "change": a["change"]})
    return out or None


def get_market_snapshot(data: list[dict] | None = None) -> str | None:
    if data is None:
        data = get_market_data()
    if not data:
        return None
    lines = [f"- {d['label']}: {d['price']:,.2f} ({d['change']:+.2f}% no dia)" for d in data]
    return "Dados de mercado (variação no dia):\n" + "\n".join(lines)
