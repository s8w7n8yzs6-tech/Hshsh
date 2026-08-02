"""Configuração central lida a partir de variáveis de ambiente."""
from __future__ import annotations

import os

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
POST_LANGUAGE = os.getenv("POST_LANGUAGE", "português do Brasil")

PLATFORMS = [p.strip().lower() for p in os.getenv("PLATFORMS", "threads").split(",") if p.strip()]

THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")

INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Tipos de conteúdo e seus pesos na escolha aleatória.
CONTENT_TYPES = ("motivacional", "mercado", "educacional")
CONTENT_WEIGHTS = (0.35, 0.35, 0.30)

# Tipo fixo, se definido no ambiente (senão, sorteio ponderado).
POST_TYPE = os.getenv("POST_TYPE", "").strip().lower() or None
