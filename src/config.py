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

# Geração de imagem por IA (fundo fotorrealista do card). Se a chave não estiver
# presente ou a chamada falhar, o sistema volta para a cena desenhada (scene.py).
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
IMAGE_MODEL = (os.getenv("IMAGE_MODEL") or "gpt-image-1").strip()
IMAGE_QUALITY = (os.getenv("IMAGE_QUALITY") or "medium").strip()  # low | medium | high

# Fotos do assunto nos carrosséis de notícia: Pexels (alta qualidade) se houver
# chave; senão cai para o Openverse (sem chave). Chave grátis em pexels.com/api.
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()

DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Tipos de conteúdo. "mercado" = card com candlestick (só 2/dia: ouro e Nasdaq).
# "trader" = conteúdo focado no trader (identificação) — os demais posts do dia.
CONTENT_TYPES = ("trader", "mercado")

# TODOS os 20 posts do dia são CARROSSÉIS DE NOTÍCIA (ver src/news.py e
# src/decks.py): manchete forte da semana explicada em 4-5 capítulos, com foto do
# assunto e o layout alternando a cada post. Os formatos abaixo continuam
# existindo como RESERVA: entram quando não há manchete nova disponível (falha de
# rede/feed vazio) e no disparo manual com --type.
MENTALITY_FORMATS = ("foto", "citacao", "mito_verdade", "numero", "lista")
EDU_FORMATS = ("padrao", "conceito", "dica")  # nos slots pares que não são mercado
TRADER_FORMATS_ROTATION = MENTALITY_FORMATS  # compat: usado no disparo manual "trader"

# Máximo de posts que UM disparo pode recuperar de uma vez (catch-up). O cron do
# GitHub é "best-effort" e na prática dispara poucas vezes por dia (já houve dia
# com só 2 disparos), então cada disparo precisa correr atrás de vários horários
# atrasados para chegar perto dos 20/dia.
CATCHUP_MAX = int(os.getenv("CATCHUP_MAX") or "8")
# Intervalo entre posts de uma mesma rodada de recuperação, em segundos. Sem ele
# os posts atrasados saem todos no mesmo minuto (fica com cara de spam no feed).
POST_GAP_S = int(os.getenv("POST_GAP_S") or "150")
# Todos os formatos válidos (para --type manual e validação).
ALL_FORMATS = ("foto", "citacao", "lista", "mito_verdade", "numero",
               "historia", "conceito", "dica", "mercado")

# Horários dos 20 posts, em horário de Brasília (UTC-3), das 07:00 às 20:30.
SCHEDULE_BRT = [
    (7, 0), (7, 43), (8, 25), (9, 8), (9, 51),
    (10, 33), (11, 16), (11, 58), (12, 41), (13, 24),
    (14, 6), (14, 49), (15, 32), (16, 14), (16, 57),
    (17, 39), (18, 22), (19, 5), (19, 47), (20, 30),
]
# Reserva: índices dos posts de mercado (só no disparo manual --type mercado).
GOLD_SLOT_INDEX = 2      # 08:25 — Ouro
NASDAQ_SLOT_INDEX = 12   # 15:32 — Nasdaq (pregão dos EUA aberto)
BRT_OFFSET_HOURS = -3

# Tipo fixo, se definido no ambiente (senão, decidido pelo horário do slot).
POST_TYPE = os.getenv("POST_TYPE", "").strip().lower() or None

# --- Variedade dos posts (evita repetição) --------------------------------
# Ângulos distintos para os posts de trader. O ângulo é escolhido por
# (slot + dia do ano), então não repete no mesmo dia e roda ao longo dos dias.
TRADER_ANGLES = [
    "a ansiedade antes de abrir uma operação",
    "a tentação de tentar recuperar rápido um prejuízo (revenge trade)",
    "respeitar o stop mesmo quando dói",
    "a paciência de esperar o setup certo aparecer",
    "o medo de ficar de fora (FOMO)",
    "operar demais (overtrading) e o cansaço mental",
    "a solidão de quem opera sozinho em casa",
    "acordar cedo para acompanhar a abertura do mercado",
    "controlar a ganância depois de um bom lucro",
    "a importância de manter um diário de operações",
    "aceitar que ter perdas faz parte do jogo",
    "disciplina no gerenciamento de risco",
    "a montanha-russa emocional de um dia de operações",
    "comemorar as pequenas evoluções, não só os grandes dias",
    "parar de se comparar com outros traders",
    "a diferença entre sorte pontual e consistência",
    "desligar as telas para descansar a mente",
    "o peso psicológico de segurar uma posição aberta",
    "confiar no próprio plano em vez de improvisar",
    "não mover o stop no calor da emoção",
    "estudar e revisar operações no fim de semana",
    "acertar a análise mas errar na execução",
    "lidar com dias de lateralização e tédio no gráfico",
    "a euforia perigosa depois de vários acertos seguidos",
    "reduzir o tamanho da posição quando está em dúvida",
    "a importância de dormir bem para operar melhor",
    "não operar por impulso logo após uma notícia",
    "rever operações passadas com honestidade",
    "bater a meta do dia e ter a disciplina de parar",
    "resistir ao 'só mais uma operação'",
    "separar a vida pessoal do resultado do dia",
    "a paciência de anos até virar um trader consistente",
    "respeitar o horário de encerrar o dia de operações",
    "a diferença entre ser trader e ser apostador",
    "manter a rotina de estudo mesmo desmotivado",
    "a gratidão por evoluir aos poucos, um dia de cada vez",
]
TRADER_FORMATS = [
    "uma pergunta direta ao leitor",
    "uma frase curta e de impacto",
    "uma mini-reflexão em 2 ou 3 frases",
    "uma situação do dia a dia com a qual o trader se identifica",
    "uma verdade honesta que poucos falam",
    "um lembrete acolhedor e encorajador",
]
# Enfoques para variar os posts de mercado.
MARKET_ANGLES = [
    "destaque a variação do dia e o que ela indica, de forma neutra",
    "comente a amplitude entre a máxima e a mínima do período",
    "fale sobre a volatilidade recente nos candles de 30 min",
    "comente, sem prever direção, se o dia teve mais força compradora ou vendedora",
]
