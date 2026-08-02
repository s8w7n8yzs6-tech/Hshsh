"""Temas visuais por tipo de conteúdo (cores usadas no card e no gráfico)."""
from __future__ import annotations

THEMES = {
    "trader": {
        "badge": "TRADER",
        "bg_top": (18, 28, 40),
        "bg_bottom": (8, 13, 20),
        "accent": (45, 212, 191),   # teal
    },
    "mercado": {
        "badge": "MERCADO",
        "bg_top": (10, 30, 55),
        "bg_bottom": (6, 14, 26),
        "accent": (56, 189, 248),   # ciano
    },
}


def theme_for(content_type: str) -> dict:
    return THEMES.get(content_type, THEMES["trader"])


def accent_hex(content_type: str) -> str:
    r, g, b = theme_for(content_type)["accent"]
    return f"#{r:02x}{g:02x}{b:02x}"
