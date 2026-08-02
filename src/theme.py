"""Temas visuais por tipo de conteúdo (cores usadas no card e no gráfico)."""
from __future__ import annotations

THEMES = {
    "motivacional": {
        "badge": "MINDSET",
        "bg_top": (43, 22, 15),
        "bg_bottom": (17, 9, 7),
        "accent": (251, 146, 60),   # laranja
    },
    "mercado": {
        "badge": "MERCADO",
        "bg_top": (10, 30, 55),
        "bg_bottom": (6, 14, 26),
        "accent": (56, 189, 248),   # ciano
    },
    "educacional": {
        "badge": "EDUCATIVO",
        "bg_top": (30, 20, 55),
        "bg_bottom": (13, 9, 26),
        "accent": (167, 139, 250),  # roxo
    },
}


def theme_for(content_type: str) -> dict:
    return THEMES.get(content_type, THEMES["educacional"])


def accent_hex(content_type: str) -> str:
    r, g, b = theme_for(content_type)["accent"]
    return f"#{r:02x}{g:02x}{b:02x}"
