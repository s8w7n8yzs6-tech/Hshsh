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

DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Tipos de conteúdo. "mercado" = card com candlestick (só 2/dia: ouro e Nasdaq).
# "trader" = conteúdo focado no trader (identificação) — os demais posts do dia.
CONTENT_TYPES = ("trader", "mercado")

# Formatos que se revezam nos posts de trader (dão variedade ao feed). O formato
# de cada slot é escolhido por (slot + dia), então posts vizinhos são diferentes
# e a ordem muda a cada dia. "foto" usa imagem de IA; os demais são desenhados.
# Metade do dia é DESENVOLVIMENTO (educativo: padrões/gráficos/conceitos/dicas) e
# metade é MENTALIDADE (o lado psicológico). Slots pares = educativo, ímpares =
# mentalidade → 10 e 10, intercalados no feed.
MENTALITY_FORMATS = ("foto", "citacao", "mito_verdade", "numero", "lista")
EDU_FORMATS = ("padrao", "conceito", "dica")  # nos slots pares que não são mercado
TRADER_FORMATS_ROTATION = MENTALITY_FORMATS  # compat: usado no disparo manual "trader"

# Máximo de posts que UM disparo pode recuperar de uma vez (catch-up). Se o GitHub
# disparar poucas vezes no dia, cada disparo corre atrás de vários horários
# atrasados, para chegar perto dos 20/dia. Em dias normais fica ~1 por disparo.
CATCHUP_MAX = int(os.getenv("CATCHUP_MAX") or "4")
# Todos os formatos válidos (para --type manual e validação).
ALL_FORMATS = ("foto", "citacao", "lista", "mito_verdade", "numero",
               "historia", "conceito", "dica", "mercado")

# Horários dos 20 posts, em horário de Brasília (UTC-3), das 07:00 às 20:30.
# O tipo de cada post é decidido pelo slot mais próximo do horário atual.
SCHEDULE_BRT = [
    (7, 0), (7, 43), (8, 25), (9, 8), (9, 51),
    (10, 33), (11, 16), (11, 58), (12, 41), (13, 24),
    (14, 6), (14, 49), (15, 32), (16, 14), (16, 57),
    (17, 39), (18, 22), (19, 5), (19, 47), (20, 30),
]
# Índices (na lista acima) dos 2 posts de mercado do dia:
GOLD_SLOT_INDEX = 2      # 08:25 — Ouro (slot par = educativo)
NASDAQ_SLOT_INDEX = 12   # 15:32 — Nasdaq (pregão dos EUA aberto; slot par)
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
