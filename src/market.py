"""Dados de mercado reais para Ouro (XAU/USD) e Nasdaq 100, via Yahoo Finance.

Endpoint público, sem chave. A variação é "no dia" (preço atual vs. fechamento
anterior). Os números vêm de dados reais, não são inventados.
"""
from __future__ import annotations

import requests

# Ativos acompanhados. GC=F (ouro futuro) é usado como proxy do XAU/USD spot.
_ASSETS = [
    {"symbol": "GC=F", "label": "Ouro (XAU/USD)", "short": "XAU/USD"},
    {"symbol": "^NDX", "label": "Nasdaq 100", "short": "NASDAQ"},
]
_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
_HEADERS = {"User-Agent": "Mozilla/5.0"}


def _fetch_one(symbol: str, timeout: int):
    resp = requests.get(
        _URL.format(symbol=symbol),
        params={"range": "5d", "interval": "1d"},
        headers=_HEADERS,
        timeout=timeout,
    )
    resp.raise_for_status()
    meta = resp.json()["chart"]["result"][0]["meta"]
    price = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    if price is None or not prev:
        return None
    change = (price - prev) / prev * 100
    return float(price), float(change)


def get_market_data(timeout: int = 15) -> list[dict] | None:
    """Retorna [{"label","short","price","change"}] ou None se nada for obtido."""
    out = []
    for asset in _ASSETS:
        try:
            result = _fetch_one(asset["symbol"], timeout)
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            result = None
        if not result:
            continue
        price, change = result
        out.append(
            {"label": asset["label"], "short": asset["short"], "price": price, "change": change}
        )
    return out or None


def get_market_snapshot(data: list[dict] | None = None) -> str | None:
    """Resumo textual (contexto factual para o modelo)."""
    if data is None:
        data = get_market_data()
    if not data:
        return None
    lines = [
        f"- {d['label']}: {d['price']:,.2f} ({d['change']:+.2f}% no dia)"
        for d in data
    ]
    return "Dados de mercado (variação no dia):\n" + "\n".join(lines)
