"""Configuração central lida a partir de variáveis de ambiente."""
from __future__ import annotations

import os

# Usa `or default` para que uma variável definida como string vazia
# (comum no GitHub Actions quando a variable não existe) caia no padrão.
ANTHROPIC_MODEL = (os.getenv("ANTHROPIC_MODEL") or "claude-sonnet-5").strip()
POST_LANGUAGE = (os.getenv("POST_LANGUAGE") or "português do Brasil").strip()

# @ (handle) acrescentado ao final de cada post como assinatura.
POST_HANDLE = (os.getenv("POST_HANDLE") or "@thiago.cunhaff").strip()

PLATFORMS = [p.strip().lower() for p in (os.getenv("PLATFORMS") or "threads").split(",") if p.strip()]

THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")

INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Tipos de conteúdo e seus pesos na escolha aleatória.
# Mercado (ouro/Nasdaq, com candlestick) tem o maior peso — é o foco.
CONTENT_TYPES = ("motivacional", "mercado", "educacional")
CONTENT_WEIGHTS = (0.25, 0.50, 0.25)

# Tipo fixo, se definido no ambiente (senão, sorteio ponderado).
POST_TYPE = os.getenv("POST_TYPE", "").strip().lower() or None
