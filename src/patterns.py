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
]


def pick_pattern(i: int) -> dict:
    return PATTERNS[i % len(PATTERNS)]


def pick_concept(i: int) -> str:
    return CONCEPTS[i % len(CONCEPTS)]
