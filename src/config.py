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

# .strip() protege contra espaços/tabs/quebras acidentais coladas no Secret
# (um TAB no INSTAGRAM_USER_ID, por ex., quebrava a URL da API com %09).
THREADS_USER_ID = os.getenv("THREADS_USER_ID", "").strip()
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "").strip()

INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "").strip()
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "").strip()

DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Tipos de conteúdo. "mercado" = card com candlestick (só 2/dia: ouro e Nasdaq).
# "trader" = conteúdo focado no trader (identificação) — os demais posts do dia.
CONTENT_TYPES = ("trader", "mercado")

# Horários dos 20 posts, em horário de Brasília (UTC-3), das 07:00 às 20:30.
# O tipo de cada post é decidido pelo slot mais próximo do horário atual.
SCHEDULE_BRT = [
    (7, 0), (7, 43), (8, 25), (9, 8), (9, 51),
    (10, 33), (11, 16), (11, 58), (12, 41), (13, 24),
    (14, 6), (14, 49), (15, 32), (16, 14), (16, 57),
    (17, 39), (18, 22), (19, 5), (19, 47), (20, 30),
]
# Índices (na lista acima) dos 2 posts de mercado do dia:
GOLD_SLOT_INDEX = 2      # 08:25 — Ouro
NASDAQ_SLOT_INDEX = 13   # 16:14 — Nasdaq (pregão dos EUA aberto)
BRT_OFFSET_HOURS = -3

# Tipo fixo, se definido no ambiente (senão, decidido pelo horário do slot).
POST_TYPE = os.getenv("POST_TYPE", "").strip().lower() or None
