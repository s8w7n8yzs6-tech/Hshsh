"""Dados de mercado reais (cripto) via API pública do CoinGecko — sem chave."""
from __future__ import annotations

import requests

# id do CoinGecko -> (rótulo completo, sigla)
_COINS = {
    "bitcoin": ("Bitcoin (BTC)", "BTC"),
    "ethereum": ("Ethereum (ETH)", "ETH"),
    "solana": ("Solana (SOL)", "SOL"),
}
_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_market_data(timeout: int = 15) -> list[dict] | None:
    """Retorna dados estruturados de preço/variação 24h, ou None em falha.

    Cada item: {"label", "short", "price", "change"}. Serve tanto para o texto
    quanto para o gráfico — os números vêm de dados reais, não são inventados.
    """
    params = {
        "ids": ",".join(_COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    try:
        resp = requests.get(_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None

    out = []
    for coin_id, (label, short) in _COINS.items():
        info = data.get(coin_id)
        if not info:
            continue
        price = info.get("usd")
        change = info.get("usd_24h_change")
        if price is None or change is None:
            continue
        out.append({"label": label, "short": short, "price": float(price), "change": float(change)})
    return out or None


def get_market_snapshot(data: list[dict] | None = None) -> str | None:
    """Resumo textual dos preços e variação 24h (contexto factual para o modelo)."""
    if data is None:
        data = get_market_data()
    if not data:
        return None
    lines = [
        f"- {d['label']}: US$ {d['price']:,.2f} ({d['change']:+.2f}% em 24h)"
        for d in data
    ]
    return "Dados de mercado (últimas 24h):\n" + "\n".join(lines)
