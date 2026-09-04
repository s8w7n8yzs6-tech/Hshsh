"""Memória anti-repetição: histórico de posts guardado no repositório.

Cada post publicado é registrado em `state/history.json`. Antes de gerar um novo
post, as chamadas (headlines) recentes são passadas ao modelo com a instrução de
não repeti-las. O arquivo é commitado de volta pelo workflow após publicar.
"""
from __future__ import annotations

import json
import os

HISTORY_PATH = os.path.join("state", "history.json")


def _load(path: str) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def recent_headlines(n: int = 20, path: str | None = None) -> list[str]:
    """Últimas N headlines publicadas (para o modelo evitar repetir)."""
    return [e.get("headline", "") for e in _load(path or HISTORY_PATH)[-n:] if e.get("headline")]


# 20 posts/dia × ~100 dias. Precisa ser grande: é essa lista que impede uma
# manchete (ou um assunto do acervo) de voltar a virar post meses depois.
MAX_ITEMS = 2000


def append(entry: dict, max_items: int = MAX_ITEMS, path: str | None = None) -> None:
    """Adiciona um post ao histórico, mantendo no máximo `max_items` registros."""
    path = path or HISTORY_PATH
    data = _load(path)
    data.append(entry)
    data = data[-max_items:]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
