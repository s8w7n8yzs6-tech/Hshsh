"""Biblioteca de padrões gráficos e conceitos para os posts educativos.

Cada padrão traz um DIAGRAMA esquemático (didático, não são dados reais de
mercado) — desenhado por src/edu.py — mais uma dica do que o modelo deve
explicar. Tudo em tom educativo: ensina o que é, sem recomendar operação.
"""
from __future__ import annotations

# Padrões com diagrama. tipo "candles": lista de velas (o,h,l,c) normalizadas
# 0..1 (1 = topo). tipo "linha": um caminho de preço + linhas horizontais e/ou
# de tendência. Cores: verde = alta, vermelho = baixa.
PATTERNS = [
    {
        "key": "martelo",
        "nome": "Martelo",
        "tipo": "candles",
        "candles": [
            (0.86, 0.89, 0.81, 0.83), (0.83, 0.85, 0.75, 0.77),
            (0.77, 0.79, 0.69, 0.71), (0.71, 0.73, 0.62, 0.64),
            (0.60, 0.63, 0.40, 0.615), (0.63, 0.74, 0.62, 0.72),
        ],
        "hint": "candle de corpo pequeno no topo e pavio inferior longo, que aparece após uma queda; é estudado como possível sinal de enfraquecimento da baixa.",
    },
    {
        "key": "estrela_cadente",
        "nome": "Estrela cadente",
        "tipo": "candles",
        "candles": [
            (0.14, 0.20, 0.11, 0.18), (0.18, 0.28, 0.17, 0.26),
            (0.26, 0.36, 0.25, 0.34), (0.34, 0.44, 0.33, 0.42),
            (0.46, 0.66, 0.45, 0.475), (0.44, 0.46, 0.34, 0.36),
        ],
        "hint": "candle de corpo pequeno embaixo e pavio superior longo, após uma alta; é estudado como possível sinal de enfraquecimento da alta.",
    },
    {
        "key": "engolfo_alta",
        "nome": "Engolfo de alta",
        "tipo": "candles",
        "candles": [
            (0.72, 0.75, 0.66, 0.68), (0.66, 0.69, 0.58, 0.60),
            (0.58, 0.61, 0.52, 0.545), (0.50, 0.66, 0.48, 0.64),
            (0.64, 0.72, 0.62, 0.70),
        ],
        "hint": "uma vela de alta que 'engole' totalmente a vela de baixa anterior; estudado como possível sinal de reversão para cima.",
    },
    {
        "key": "doji",
        "nome": "Doji",
        "tipo": "candles",
        "candles": [
            (0.30, 0.34, 0.26, 0.33), (0.33, 0.44, 0.32, 0.43),
            (0.43, 0.55, 0.42, 0.54), (0.585, 0.70, 0.48, 0.59),
            (0.57, 0.60, 0.46, 0.48),
        ],
        "hint": "vela em que abertura e fechamento quase coincidem (corpo minúsculo); mostra indecisão entre compradores e vendedores.",
    },
    {
        "key": "suporte_resistencia",
        "nome": "Suporte e resistência",
        "tipo": "linha",
        "path": [(0.03, 0.30), (0.15, 0.72), (0.28, 0.30), (0.42, 0.73),
                 (0.56, 0.29), (0.70, 0.72), (0.84, 0.31), (0.97, 0.60)],
        "hlines": [("Resistência", 0.74, "down"), ("Suporte", 0.28, "up")],
        "hint": "regiões em que o preço costuma parar de subir (resistência) ou de cair (suporte); base para entender onde o mercado 'respeita' níveis.",
    },
    {
        "key": "topo_duplo",
        "nome": "Topo duplo",
        "tipo": "linha",
        "path": [(0.03, 0.30), (0.22, 0.78), (0.37, 0.52), (0.52, 0.79),
                 (0.68, 0.50), (0.82, 0.34), (0.97, 0.22)],
        "hlines": [("Resistência", 0.79, "down"), ("Linha de pescoço", 0.51, "neutral")],
        "hint": "dois topos na mesma região seguidos de queda abaixo da 'linha de pescoço'; estudado como possível sinal de reversão de alta para baixa.",
    },
    {
        "key": "triangulo",
        "nome": "Triângulo",
        "tipo": "linha",
        "path": [(0.03, 0.28), (0.16, 0.72), (0.30, 0.36), (0.44, 0.66),
                 (0.58, 0.44), (0.72, 0.60), (0.85, 0.50), (0.97, 0.54)],
        "trendlines": [((0.10, 0.76), (0.97, 0.56)), ((0.10, 0.30), (0.97, 0.50))],
        "hint": "as máximas e mínimas se aproximam formando um triângulo (compressão); mostra um mercado indeciso acumulando força.",
    },
    {
        "key": "rompimento",
        "nome": "Rompimento",
        "tipo": "linha",
        "path": [(0.03, 0.45), (0.14, 0.55), (0.25, 0.44), (0.36, 0.56),
                 (0.47, 0.45), (0.58, 0.55), (0.69, 0.52), (0.80, 0.74), (0.97, 0.86)],
        "hlines": [("Resistência", 0.58, "down")],
        "hint": "o preço fica 'preso' abaixo de uma resistência e depois a ultrapassa com força; conceito de rompimento de nível.",
    },
    {
        "key": "fundo_duplo",
        "nome": "Fundo duplo",
        "tipo": "linha",
        "path": [(0.03, 0.70), (0.22, 0.24), (0.40, 0.50), (0.60, 0.25),
                 (0.80, 0.64), (0.97, 0.78)],
        "hlines": [("Suporte", 0.25, "up"), ("Linha de pescoço", 0.50, "neutral")],
        "hint": "dois fundos na mesma região seguidos de alta acima da 'linha de pescoço'; estudado como possível reversão de baixa para alta.",
    },
    {
        "key": "oco",
        "nome": "Ombro-cabeça-ombro",
        "tipo": "linha",
        "path": [(0.03, 0.32), (0.16, 0.62), (0.28, 0.44), (0.42, 0.80),
                 (0.56, 0.42), (0.70, 0.62), (0.84, 0.40), (0.97, 0.26)],
        "hlines": [("Linha de pescoço", 0.43, "neutral")],
        "hint": "três topos com o do meio (a 'cabeça') mais alto; estudado como possível sinal de reversão de alta para baixa.",
    },
    {
        "key": "bandeira",
        "nome": "Bandeira",
        "tipo": "linha",
        "path": [(0.03, 0.24), (0.14, 0.74), (0.26, 0.60), (0.38, 0.70),
                 (0.50, 0.56), (0.62, 0.66), (0.74, 0.54), (0.86, 0.78), (0.97, 0.88)],
        "hint": "uma forte alta, um respiro curto de correção (a 'bandeira') e a retomada do movimento; padrão de continuação.",
    },
    {
        "key": "canal_alta",
        "nome": "Canal de alta",
        "tipo": "linha",
        "path": [(0.03, 0.30), (0.16, 0.50), (0.30, 0.36), (0.44, 0.58),
                 (0.58, 0.46), (0.72, 0.68), (0.86, 0.56), (0.97, 0.74)],
        "trendlines": [((0.05, 0.38), (0.97, 0.80)), ((0.05, 0.24), (0.97, 0.62))],
        "hint": "máximas e mínimas subindo entre duas linhas paralelas; mostra uma tendência de alta organizada dentro de um canal.",
    },
]

# Estratégias de trade (educativas). Cada uma vira um post que ENSINA como a
# estratégia funciona e o que observar — sem recomendar operação nem prometer
# resultado. Formato de texto (card de conceito).
STRATEGIES = [
    ("Pullback na média móvel", "em uma tendência, esperar o preço recuar até uma média móvel antes de continuar o movimento"),
    ("Rompimento de resistência", "quando o preço ultrapassa com força uma região que antes o segurava (breakout)"),
    ("Rompimento de range", "operar a saída de uma consolidação lateral (o preço 'preso' entre dois níveis)"),
    ("Price action em suporte/resistência", "ler o comportamento das velas ao chegar em níveis importantes, sem indicadores"),
    ("Cruzamento de médias móveis", "usar o cruzamento de uma média rápida com uma lenta para ler a mudança de tendência"),
    ("Retração de Fibonacci", "usar os níveis de Fibonacci para mapear até onde uma correção pode ir"),
    ("Operar a favor da tendência", "o conceito de trend following: alinhar as entradas com a direção dominante"),
    ("Setup de reversão com confirmação", "esperar um candle de confirmação antes de operar uma possível virada"),
    ("Inside bar", "uma barra 'dentro' da anterior indicando pausa e possível continuação do movimento"),
    ("Teste de suporte (segundo toque)", "por que o segundo toque em um suporte costuma ser mais observado que o primeiro"),
    ("Rompimento de linha de tendência", "o que significa o preço romper uma LTA ou LTB traçada no gráfico"),
    ("Média móvel como suporte dinâmico", "como uma média pode funcionar de 'piso' móvel dentro de uma tendência de alta"),
    ("Divergência entre preço e indicador", "quando o preço faz novo topo mas o indicador não acompanha (sinal de enfraquecimento)"),
    ("Bandeira de continuação", "um respiro curto depois de um movimento forte, antes de a tendência retomar"),
    ("Pivô de alta e de baixa", "o conceito de ponto de virada usado para marcar entradas e stops"),
    ("Projeção de alvo pela medida do padrão", "estimar um objetivo do movimento pela própria altura da figura no gráfico"),
    ("Trailing stop", "mover o stop conforme o lucro avança para proteger ganhos"),
    ("Gap de abertura", "o que é o gap e por que ele merece atenção no início do pregão"),
    ("Congestão e rompimento", "acumulação de preço em uma faixa estreita antes de um movimento maior"),
    ("Confluência de sinais", "por que juntar dois ou três fatores aumenta a qualidade de uma leitura"),
    ("Reteste do rompimento", "quando o preço volta para 'confirmar' o nível que acabou de romper"),
    ("Operar apenas o setup do seu plano", "a disciplina de esperar exatamente o cenário que você estudou"),
]

# Indicadores técnicos (educativos).
INDICATORS = [
    ("Médias móveis", "a média do preço em X períodos, usada para suavizar o gráfico e ler a tendência"),
    ("IFR (RSI)", "o Índice de Força Relativa, que mede se um ativo está muito comprado ou muito vendido"),
    ("MACD", "a convergência/divergência de médias, usada para ler força e mudança de tendência"),
    ("Bandas de Bollinger", "bandas que se abrem e fecham conforme a volatilidade do preço"),
    ("Estocástico", "um oscilador que compara o fechamento com a faixa de preço do período"),
    ("Volume", "quantas negociações aconteceram — usado para confirmar a força de um movimento"),
    ("VWAP", "o preço médio ponderado pelo volume, referência muito usada no intraday"),
    ("ATR", "o Average True Range, que mede a volatilidade média (útil para dimensionar o stop)"),
    ("OBV", "o On Balance Volume, que soma/subtrai volume para ler pressão de compra e venda"),
    ("ADX", "um indicador que mede a FORÇA da tendência (sem dizer a direção)"),
    ("Suporte e resistência por volume", "identificar níveis onde passou muito volume negociado"),
    ("Ichimoku (visão geral)", "um sistema japonês que mostra tendência, suporte e resistência de uma vez"),
]

# Temas para posts de DICAS (lista pra salvar), educativos e práticos.
DICA_THEMES = [
    "montar um plano de trade antes de operar",
    "dimensionar o tamanho da posição pelo risco",
    "definir e respeitar o stop",
    "escolher poucos ativos para acompanhar",
    "organizar a rotina de estudo do trader",
    "manter um diário de operações",
    "revisar as operações no fim de semana",
    "evitar os erros mais comuns do iniciante",
    "usar mais de um tempo gráfico na análise",
    "controlar o número de operações por dia",
    "preparar o pré-mercado antes de operar",
    "proteger os lucros de um bom dia",
]

# Conceitos/dicas educativas (sem diagrama próprio; formato de texto/lista).
CONCEPTS = [
    "gerenciamento de risco: arriscar só uma pequena parte da banca por operação",
    "a relação risco/retorno (por que buscar ganho maior que a perda arriscada)",
    "o que é o stop loss e por que ele protege a conta",
    "a diferença entre suporte e resistência na prática",
    "o papel do volume para confirmar um movimento",
    "o que é tendência de alta, de baixa e lateral",
    "por que operar a favor da tendência costuma ser mais seguro",
    "a importância dos diferentes tempos gráficos (timeframes)",
    "o perigo da alavancagem alta para iniciantes",
    "por que ter um plano de trade escrito antes de operar",
    "como o espalhamento (spread) e custos afetam o resultado",
    "o conceito de pullback (respiro) dentro de uma tendência",
    "por que não mover o stop no meio da operação",
    "o que é liquidez e por que operar ativos líquidos",
    "a diferença entre análise técnica e análise fundamentalista",
    "por que backtestar e revisar as operações passadas",
    "o que é OHLC (abertura, máxima, mínima, fechamento) de um candle",
    "o que o pavio (sombra) de um candle revela",
    "o que são topos e fundos ascendentes e descendentes",
    "a diferença entre corpo e pavio na leitura da vela",
    "o que é o book de ofertas (livro de ordens)",
    "o que é slippage (deslizamento na execução)",
    "o que é drawdown e por que acompanhá-lo",
    "a diferença entre day trade, swing trade e position",
    "o que é volatilidade e como ela muda o risco",
    "por que o horário do pregão influencia a liquidez",
]

_STOP = {"a", "o", "e", "de", "do", "da", "que", "na", "no", "um", "uma", "por", "para", "com", "os", "as"}


def _slug(text: str, n: int = 4) -> str:
    """Chave estável e curta a partir de um texto (para marcar 'já usado')."""
    import re
    import unicodedata

    t = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode()
    words = [w for w in re.findall(r"[a-z0-9]+", t) if w not in _STOP]
    return "-".join(words[:n]) or "x"


def build_pool() -> list[dict]:
    """Acervo educativo ORDENADO e intercalado, cada assunto com chave única.

    Cada item: {key, fmt, badge, nome, hint, pattern?}. A seleção em post.py pega o
    próximo item cuja `key` ainda não apareceu na memória — assim NADA se repete
    até o acervo inteiro ser usado (dezenas de assuntos distintos).
    """
    cats: list[list[dict]] = []

    cats.append([
        {"key": f"pat:{p['key']}", "fmt": "padrao", "badge": "APRENDA UM PADRÃO",
         "nome": p["nome"], "hint": p["hint"], "pattern": p}
        for p in PATTERNS
    ])
    cats.append([
        {"key": f"est:{_slug(nome)}", "fmt": "conceito", "badge": "ESTRATÉGIA",
         "nome": nome, "hint": hint}
        for nome, hint in STRATEGIES
    ])
    cats.append([
        {"key": f"ind:{_slug(nome)}", "fmt": "conceito", "badge": "INDICADOR",
         "nome": nome, "hint": hint}
        for nome, hint in INDICATORS
    ])
    cats.append([
        {"key": f"con:{_slug(c)}", "fmt": "conceito", "badge": "APRENDA",
         "nome": "", "hint": c}
        for c in CONCEPTS
    ])
    cats.append([
        {"key": f"dic:{_slug(t)}", "fmt": "dica", "badge": "APRENDA",
         "nome": "", "hint": t}
        for t in DICA_THEMES
    ])

    # Intercala as categorias (round-robin) para o feed ficar variado.
    pool: list[dict] = []
    for i in range(max(len(c) for c in cats)):
        for c in cats:
            if i < len(c):
                pool.append(c[i])
    return pool


def pick_pattern(i: int) -> dict:
    return PATTERNS[i % len(PATTERNS)]


def pick_concept(i: int) -> str:
    return CONCEPTS[i % len(CONCEPTS)]
