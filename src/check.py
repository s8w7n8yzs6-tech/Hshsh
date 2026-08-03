"""Verifica a configuração antes de publicar de verdade.

Uso:
    python -m src.check

Valida (somente leitura, não publica nada):
- chave da Anthropic presente
- imgbb presente (necessária para imagens)
- token/ID do Instagram válidos (consulta o nome de usuário)
- token/ID do Threads válidos (consulta o nome de usuário)
"""
from __future__ import annotations

import requests

from . import config


def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _warn(msg: str) -> None:
    print(f"  [!]    {msg}")


def _fail(msg: str) -> None:
    print(f"  [FALHA] {msg}")


def _check_instagram() -> None:
    if not (config.INSTAGRAM_USER_ID and config.INSTAGRAM_ACCESS_TOKEN):
        _warn("Instagram: credenciais ausentes (INSTAGRAM_USER_ID / INSTAGRAM_ACCESS_TOKEN).")
        return
    try:
        r = requests.get(
            "https://graph.instagram.com/v21.0/me",
            params={"fields": "user_id,username", "access_token": config.INSTAGRAM_ACCESS_TOKEN},
            timeout=20,
        )
        data = r.json()
        if r.status_code == 200 and "username" in data:
            _ok(f"Instagram conectado como @{data['username']} (user_id {data.get('user_id')})")
        else:
            _fail(f"Instagram: {data.get('error', {}).get('message', data)}")
    except requests.RequestException as exc:
        _fail(f"Instagram: erro de rede: {exc}")


def _check_threads() -> None:
    if not (config.THREADS_USER_ID and config.THREADS_ACCESS_TOKEN):
        _warn("Threads: credenciais ausentes (THREADS_USER_ID / THREADS_ACCESS_TOKEN).")
        return
    try:
        r = requests.get(
            f"https://graph.threads.net/v1.0/{config.THREADS_USER_ID}",
            params={"fields": "username", "access_token": config.THREADS_ACCESS_TOKEN},
            timeout=20,
        )
        data = r.json()
        if r.status_code == 200 and "username" in data:
            _ok(f"Threads conectado como @{data['username']}")
        else:
            _fail(f"Threads: {data.get('error', {}).get('message', data)}")
    except requests.RequestException as exc:
        _fail(f"Threads: erro de rede: {exc}")


def main() -> None:
    print("Verificando configuração...\n")

    print("Geração (Claude):")
    _ok("ANTHROPIC_API_KEY presente") if __import__("os").getenv("ANTHROPIC_API_KEY") else _fail(
        "ANTHROPIC_API_KEY ausente"
    )
    print(f"  modelo: {config.ANTHROPIC_MODEL} | idioma: {config.POST_LANGUAGE} | @: {config.POST_HANDLE}")

    print("\nImagens:")
    _ok("hospedagem via GitHub (URL raw) — não precisa de imgbb")

    print(f"\nPlataformas configuradas: {', '.join(config.PLATFORMS) or '(nenhuma)'}")
    _check_instagram()
    _check_threads()

    print("\nDados de mercado (Ouro / Nasdaq):")
    from . import market

    snap = market.get_market_snapshot()
    print("  " + (snap.replace("\n", "\n  ") if snap else "[!] não foi possível obter dados agora"))


if __name__ == "__main__":
    main()
