"""Dados de mercado reais (cripto) via API pública do CoinGecko — sem chave."""
from __future__ import annotations

import requests

_COINS = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
}
_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_market_snapshot(timeout: int = 15) -> str | None:
    """Retorna um resumo textual dos preços e variação em 24h, ou None em falha.

    O texto serve de contexto factual para o modelo — os números vêm de dados
    reais, não são inventados.
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

    lines = []
    for coin_id, label in _COINS.items():
        info = data.get(coin_id)
        if not info:
            continue
        price = info.get("usd")
        change = info.get("usd_24h_change")
        if price is None or change is None:
            continue
        lines.append(f"- {label}: US$ {price:,.2f} ({change:+.2f}% em 24h)")

    if not lines:
        return None
    return "Dados de mercado (últimas 24h):\n" + "\n".join(lines)
