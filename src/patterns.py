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
    {
        "key": "engolfo_baixa",
        "nome": "Engolfo de baixa",
        "tipo": "candles",
        "candles": [(0.30, 0.34, 0.28, 0.33), (0.33, 0.43, 0.32, 0.41),
                    (0.41, 0.47, 0.40, 0.45), (0.62, 0.64, 0.44, 0.46),
                    (0.46, 0.48, 0.37, 0.39)],
        "hint": "uma vela de baixa que 'engole' totalmente a vela de alta anterior; estudado como possível reversão para baixo.",
    },
    {
        "key": "martelo_invertido",
        "nome": "Martelo invertido",
        "tipo": "candles",
        "candles": [(0.86, 0.89, 0.81, 0.83), (0.80, 0.82, 0.72, 0.74),
                    (0.72, 0.74, 0.64, 0.66), (0.55, 0.75, 0.54, 0.57),
                    (0.57, 0.66, 0.56, 0.64)],
        "hint": "corpo pequeno embaixo com pavio superior longo, após queda; estudado como possível reversão de baixa para alta.",
    },
    {
        "key": "estrela_da_noite",
        "nome": "Estrela da noite",
        "tipo": "candles",
        "candles": [(0.30, 0.34, 0.28, 0.33), (0.40, 0.58, 0.39, 0.56),
                    (0.60, 0.66, 0.58, 0.61), (0.55, 0.57, 0.40, 0.42)],
        "hint": "três velas no topo (alta forte, indecisão e queda forte); estudada como possível reversão de alta para baixa.",
    },
    {
        "key": "tres_soldados",
        "nome": "Três soldados",
        "tipo": "candles",
        "candles": [(0.30, 0.36, 0.28, 0.35), (0.35, 0.50, 0.34, 0.49),
                    (0.49, 0.64, 0.48, 0.63), (0.63, 0.78, 0.62, 0.77)],
        "hint": "três velas de alta seguidas e firmes; estudadas como possível força compradora entrando.",
    },
    {
        "key": "cunha_alta",
        "nome": "Cunha ascendente",
        "tipo": "linha",
        "path": [(0.03, 0.30), (0.16, 0.52), (0.30, 0.42), (0.44, 0.62),
                 (0.58, 0.54), (0.72, 0.70), (0.86, 0.64), (0.97, 0.76)],
        "trendlines": [((0.05, 0.50), (0.97, 0.80)), ((0.05, 0.28), (0.97, 0.72))],
        "hint": "duas linhas de alta que se aproximam (cunha); estudada como possível perda de força da tendência.",
    },
    {
        "key": "canal_baixa",
        "nome": "Canal de baixa",
        "tipo": "linha",
        "path": [(0.03, 0.76), (0.16, 0.56), (0.30, 0.68), (0.44, 0.48),
                 (0.58, 0.60), (0.72, 0.40), (0.86, 0.52), (0.97, 0.34)],
        "trendlines": [((0.05, 0.80), (0.97, 0.40)), ((0.05, 0.66), (0.97, 0.26))],
        "hint": "máximas e mínimas caindo entre duas linhas paralelas; tendência de baixa organizada dentro de um canal.",
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
    ("Falso rompimento (fakeout)", "reconhecer quando o preço 'finge' romper um nível e volta, armadilha comum"),
    ("Opening Range Breakout", "usar a máxima e a mínima dos primeiros minutos do pregão como referência"),
    ("Setup 9.1 (Larry Williams)", "entrada após o preço cruzar a média móvel de 9 períodos, muito usado no Brasil"),
    ("Suportes psicológicos (números redondos)", "por que preços 'redondos' costumam atrair atenção do mercado"),
    ("Pin bar (barra de rejeição)", "uma vela de pavio longo que mostra rejeição de preço em um nível"),
    ("Retração de 50% do movimento", "observar quando uma correção devolve cerca de metade do movimento anterior"),
    ("Range trading (operar a lateral)", "trabalhar as bordas de uma faixa lateral, entre suporte e resistência"),
    ("Mean reversion (reversão à média)", "a ideia de que preços muito esticados tendem a voltar para a média"),
    ("Análise top-down", "olhar do tempo gráfico maior para o menor antes de decidir"),
    ("Confirmação em dois tempos gráficos", "alinhar a leitura de um gráfico maior com um menor"),
    ("Filtro de tendência com média longa", "usar uma média longa como 'filtro' para só operar a favor dela"),
    ("Realização parcial no primeiro alvo", "encerrar parte da posição no primeiro objetivo e deixar o resto correr"),
    ("Entrada escalonada", "montar a posição aos poucos em vez de tudo de uma vez"),
    ("Risco fixo por operação", "arriscar sempre a mesma pequena fração da conta em cada trade"),
    ("Stop técnico vs stop financeiro", "a diferença entre o stop pelo gráfico e o stop pelo valor que aceita perder"),
    ("Breakout da máxima do dia anterior", "usar a máxima do dia anterior como nível de referência"),
    ("Rompimento da máxima/mínima da semana", "acompanhar níveis semanais que muitos observam"),
    ("Pullback na linha de tendência", "o recuo do preço até uma LTA/LTB antes de continuar"),
    ("Não operar contra a tendência principal", "por que remar contra a maré costuma custar caro ao iniciante"),
    ("Operar nos horários de maior liquidez", "por que abertura e fechamento concentram mais movimento"),
    ("Swing trade em tendência", "segurando posições por dias, aproveitando movimentos maiores"),
    ("Scalping (o que é)", "operações muito rápidas buscando pequenas variações — exige foco e custo baixo"),
    ("Position trade (o que é)", "operações de semanas a meses, com foco no movimento maior"),
    ("Divergência de baixa e de alta", "a diferença entre divergência que enfraquece a alta e a que enfraquece a baixa"),
    ("Cruzamento de preço com a média", "quando o próprio preço cruza a média móvel como leitura de virada"),
    ("Rompimento com volume", "por que o volume acompanhando o rompimento aumenta a confiança na leitura"),
    ("Alvo por Fibonacci (extensão)", "usar as extensões de Fibonacci para mapear possíveis objetivos"),
    ("Consolidação após notícia", "como o preço costuma acumular antes de reagir a uma notícia importante"),
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
    ("Média simples x exponencial", "a diferença entre a SMA e a EMA e por que a EMA reage mais rápido"),
    ("CCI (Commodity Channel Index)", "um oscilador que mede o quão longe o preço está da sua média"),
    ("Williams %R", "um oscilador de sobrecompra e sobrevenda parecido com o estocástico"),
    ("Momentum", "mede a velocidade da variação do preço para ler força do movimento"),
    ("ROC (Rate of Change)", "mostra em % o quanto o preço mudou em relação a X períodos atrás"),
    ("Parabolic SAR", "pontos que acompanham a tendência e ajudam a visualizar possível virada"),
    ("Pivot Points", "níveis de suporte e resistência calculados a partir do pregão anterior"),
    ("Volume Profile", "mostra em quais preços houve mais volume negociado (não no tempo, no preço)"),
    ("MFI (Money Flow Index)", "um 'RSI com volume', que mede a pressão de entrada e saída de dinheiro"),
    ("Bandas de Keltner", "bandas baseadas na volatilidade (ATR) em torno de uma média"),
    ("Supertrend", "um indicador de tendência que muda de cor conforme a direção dominante"),
    ("Awesome Oscillator", "compara duas médias para medir o momentum do mercado"),
    ("Desvio padrão (volatilidade)", "mede o quanto o preço costuma variar em torno da média"),
    ("ADL / Linha de acumulação", "usa volume e posição do fechamento para ler acumulação ou distribuição"),
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
    "a diferença entre corpo forte e candle de indecisão",
    "a diferença entre correção e reversão de tendência",
    "o que é um rompimento falso (fakeout)",
    "o que é o preço médio da sua posição",
    "o que é o leilão de abertura e de fechamento",
    "o que é o after market e o pré-mercado",
    "o que é circuit breaker na bolsa",
    "a diferença entre lote padrão e lote fracionário",
    "o que é margem de garantia nos derivativos",
    "o que é rolagem de contratos futuros",
    "a diferença entre mini contrato e contrato cheio",
    "o que é o VIX, o 'índice do medo'",
    "o que é correlação entre ativos",
    "o que é sazonalidade no mercado",
    "o que é o efeito manada",
    "o que é análise de fluxo (times & trades)",
    "por que o desempenho passado não garante o futuro",
    "o que é expectativa matemática (o 'edge') de uma estratégia",
    "a diferença entre taxa de acerto e payoff",
    "por que o tamanho da amostra importa nos resultados",
    "o que é overfitting ao criar uma estratégia",
    "o que é diversificação e por que ela ajuda",
    "o que são juros compostos no crescimento da conta",
    "a diferença entre gap de continuidade e de exaustão",
    "o que é força relativa entre dois ativos",
    "o que é um stop móvel (trailing stop)",
    "por que consistência vale mais que um grande acerto",
    "o que é o spread entre compra e venda",
    "o que é tendência primária, secundária e terciária",
]

# (continuação de DICA_THEMES definida acima)
DICA_THEMES += [
    "criar uma checklist antes de cada entrada",
    "definir metas realistas de evolução",
    "cuidar do sono e da saúde para operar melhor",
    "reduzir o tamanho após uma sequência de perdas",
    "separar um capital exclusivo para operar",
    "estudar os próprios erros mais que os acertos",
    "acompanhar a agenda econômica da semana",
    "ter um ritual de início e de fim de pregão",
    "trocar quantidade por qualidade de sinais",
    "definir quanto aceita perder no dia antes de parar",
    "usar conta demo para testar o que é novo",
    "medir o desempenho pelo processo, não só pelo lucro",
    "gravar a tela para revisar as operações depois",
    "revisar o plano de trade uma vez por mês",
    "estudar um ativo de cada vez, a fundo",
    "ter um plano B para queda de conexão",
    "descansar a mente depois de bater a meta",
    "não misturar o dinheiro do trade com o das contas",
    "anotar o contexto e a emoção de cada operação",
    "aumentar o risco só depois de provar consistência",
]

# Dúvidas de quem JÁ SABE o que é Forex mas ainda é iniciante (segundo estágio:
# já entende pip, lote e alavancagem, mas trava na EXECUÇÃO, no dimensionamento,
# na consistência e na mecânica). Cada item vira um post educativo que RESPONDE
# a pergunta, sem recomendar operação. Base: docs/pesquisa-duvidas-forex-iniciantes.md.
# Formato (nome=a dúvida, hint=o que explicar). Badge "DÚVIDA DE INICIANTE".
DUVIDAS_FOREX = [
    # -- Dimensionamento de posição (o cálculo que trava todo mundo) --
    ("Como calcular o tamanho do lote pelo risco?", "parte do risco em dinheiro dividido pela distância do stop em pips vezes o valor do pip; ex.: arriscar 100 num stop de 50 pips com pip de 10/lote dá 0,2 lote"),
    ("Como saber quanto vale 1 pip na minha conta?", "o valor do pip depende do par e do tamanho do lote: cerca de 10 por pip no lote padrão, 1 no mini e 0,10 no micro para a maioria dos pares em dólar"),
    ("Por que arriscar 1% se posso arriscar mais?", "o 1% mantém qualquer sequência de perdas sobrevivível; arriscar muito por trade eleva o risco de ruína e a pressão emocional que quebra o plano"),
    ("Devo usar risco fixo em % ou valor fixo?", "risco fixo em % da conta ajusta o tamanho conforme a banca cresce ou encolhe; risco em valor fixo é mais simples, mas não se adapta ao tamanho da conta"),
    ("Meu stop 'apertado' está me tirando cedo?", "stop curto reduz a perda por trade mas aumenta a chance de ser estopado pelo ruído; o stop deve caber na estrutura do gráfico, e o lote se ajusta a ele — não o contrário"),
    # -- Execução e tipos de ordem --
    ("Buy stop x buy limit: qual a diferença?", "buy limit compra ABAIXO do preço atual (esperando recuo); buy stop compra ACIMA (confirmando rompimento); um busca preço melhor, o outro busca confirmação"),
    ("A mercado ou ordem pendente: quando usar cada uma?", "a mercado entra já, no preço atual, útil quando o gatilho é agora; pendente deixa o preço vir até seu nível, evitando perseguir e pagar mais spread"),
    ("Quando mover o stop para o zero a zero (breakeven)?", "geralmente após o trade andar a favor uma distância razoável; protege de virar perda, mas mover cedo demais te tira no ruído normal do movimento"),
    ("Vale a pena realizar parcial?", "encerrar parte no primeiro alvo trava lucro e reduz a pressão; deixar o resto correr com stop no zero busca o movimento maior — é troca entre conforto e potencial"),
    ("Como funciona o trailing stop na prática?", "o stop acompanha o preço a uma distância fixa em pips, subindo numa compra e nunca descendo; protege lucro, mas se for curto demais te tira cedo"),
    # -- Consistência: 'tenho estratégia boa e ainda perco' --
    ("Tenho estratégia boa, por que ainda perco?", "quase sempre a falha é execução, não a estratégia: entrar antes de confirmar, alargar o stop, e caçar um segundo trade para recuperar destroem uma boa estratégia"),
    ("O que é overtrading e por que me sabota?", "operar demais por tédio ou impaciência aumenta custo, cansaço de decisão e força setups ruins; menos trades de qualidade batem muitos trades medianos"),
    ("Por que meu risco varia de um trade para outro?", "risco variável (um pequeno por cautela, o próximo grande porque 'parece certo') é a marca do amador; padronizar o risco por trade é o que gera consistência"),
    ("Quantas operações por dia é saudável?", "não há número mágico, mas poucas operações alinhadas ao plano batem muitas por impulso; definir um teto por dia corta o overtrading"),
    ("Como sei se minha estratégia realmente funciona?", "por uma amostra grande de trades seguindo a MESMA regra e medindo expectativa (acerto x payoff), não por dois ou três resultados recentes"),
    # -- Métricas, journal e backtest --
    ("O que é expectância (edge) e como medir?", "é o resultado médio esperado por trade: combina taxa de acerto e payoff; positiva no longo prazo é o que faz a estratégia valer a pena"),
    ("Taxa de acerto alta é sempre melhor?", "não: dá para lucrar acertando pouco se o ganho médio for bem maior que a perda; e dá para perder acertando muito se cada perda for enorme"),
    ("Por que manter um diário de operações?", "sem registrar contexto, tamanho e emoção de cada trade não há como achar o padrão dos seus erros; o journal é o que transforma prática em evolução"),
    ("Como faço um backtest sem me enganar?", "testando a mesma regra numa amostra grande sem ajustar os parâmetros até ficar 'perfeita' no passado (overfitting), que não se repete ao vivo"),
    ("O que é R múltiplo?", "medir cada resultado em múltiplos do risco inicial (1R): um ganho de 2R pagou dois riscos; pensar em R tira o foco do dinheiro e coloca no processo"),
    # -- Sessões, timing e liquidez --
    ("Qual é o melhor horário para operar?", "a sobreposição Londres–Nova York concentra o maior volume e os spreads mais estreitos; fora dela a liquidez cai e o movimento fica mais errático"),
    ("Por que o spread alarga em certos horários?", "em baixa liquidez (virada de dia, fim de sessão) e ao redor de notícias fortes o spread abre; entrar nesses momentos encarece muito a operação"),
    ("O horário muda qual par eu devo acompanhar?", "cada sessão movimenta mais certos pares; operar um par no seu horário de maior liquidez costuma dar spread menor e movimento mais limpo"),
    # -- Notícias --
    ("Como uso o calendário econômico?", "para saber quando saem dados de alto impacto (juros, inflação/CPI, emprego/NFP) que mexem no câmbio, e decidir se opera ou fica de fora naquele horário"),
    ("Devo operar na hora da notícia?", "é o momento de maior spread, slippage e reversão brusca; muitos iniciantes evitam operar no minuto do dado justamente por isso"),
    ("Por que fui estopado bem no pavio e o preço voltou?", "em picos de volatilidade (notícia, baixa liquidez) o preço faz pavios rápidos e o spread alarga, tocando stops antes de retomar; é execução, não 'perseguição'"),
    # -- Correlação e exposição --
    ("O que é correlação entre pares e por que importa?", "pares que andam juntos (ex.: vários com dólar) somam risco: abrir três posições correlacionadas é quase triplicar a mesma aposta sem perceber"),
    ("Estou diversificando ou dobrando o mesmo risco?", "abrir vários trades na mesma direção do dólar não diversifica — concentra; checar uma matriz de correlação evita empilhar risco escondido"),
    # -- Custos escondidos --
    ("Por que meu resultado veio pior que o esperado?", "quase sempre spread, swap, slippage ou comissão que não entraram na conta do trade; custo pequeno por operação vira muito em quem opera bastante"),
    ("O swap pode comer meu lucro no swing?", "sim: manter posição vários dias pode acumular swap negativo; em operações longas o custo overnight precisa entrar na conta do resultado"),
    # -- Demo para real --
    ("Por que ganho na demo e perco no real?", "na demo não há a pressão emocional do dinheiro real; medo e ganância mudam a execução — a técnica é a mesma, o gatilho psicológico não"),
    ("Como faço a transição da demo para o real?", "começando com o menor tamanho possível (micro) para sentir a emoção com risco mínimo, e só aumentando depois de provar consistência com dinheiro real"),
    ("Quanto tempo devo ficar na demo?", "até repetir o mesmo processo com resultado estável por uma amostra grande; passar cedo demais para o real costuma custar caro, ficar tempo demais adia o teste emocional"),
    # -- Gestão avançada e psicologia de segundo estágio --
    ("O que é risco de ruína?", "a probabilidade de a conta quebrar por uma sequência de perdas; risco alto por trade a dispara mesmo com estratégia lucrativa — por isso o tamanho da posição é vital"),
    ("Quando posso aumentar o tamanho da posição?", "só depois de provar consistência por uma amostra grande; aumentar por euforia após acertos seguidos é como a maioria devolve o lucro"),
    ("Devo reduzir o risco depois de perder?", "reduzir o tamanho numa sequência ruim protege o capital e a cabeça; aumentar para 'recuperar rápido' é o caminho mais curto para quebrar"),
    ("Como paro de mexer no stop no meio do trade?", "definindo stop e alvo ANTES de entrar e não tocando neles; a regra escrita tira a decisão do calor do momento, que é onde a perda pequena vira grande"),
    ("Como lido com uma sequência de perdas (drawdown)?", "esperando: drawdown faz parte de qualquer estratégia; o que importa é o tamanho dele caber no seu risco e você seguir o mesmo processo sem revidar"),
    ("Devo ter só uma estratégia ou várias?", "no começo, dominar UMA a fundo dá mais consistência que pular entre várias; trocar de método a cada perda impede qualquer uma de provar seu valor"),
    ("Qual timeframe usar já sabendo o básico?", "o maior dá o contexto e o menor a entrada; alinhar dois tempos (top-down) evita operar contra o cenário principal — mais tempo gráfico nem sempre é melhor"),
    # -- Mesa proprietária (prop firm) --
    ("O que é uma mesa proprietária (prop firm)?", "empresa que dá capital para operar após um teste pago; você opera o dinheiro dela seguindo regras e divide o lucro — o foco delas é proteção do capital"),
    ("Drawdown estático x trailing: qual a diferença?", "o estático mede a perda a partir do saldo inicial; o trailing sobe junto com o lucro e aperta o limite — é a regra que mais reprova quem passaria pelo alvo"),
    ("Vale a pena entrar numa prop firm como iniciante?", "só faz sentido com consistência já provada: as regras (meta, perda diária, trailing, janelas de notícia) reprovam quem ainda não domina gestão de risco"),
]

# MENTALIDADE do trader de segundo estágio: quem já domina o básico mas ainda
# briga com a própria cabeça. Foco em pensar em probabilidades, processo acima
# do resultado, aceitar a perda, paciência, ego e identidade. Cada item vira um
# post educativo que TRABALHA a mentalidade, sem recomendar operação.
# Base: docs/pesquisa-duvidas-forex-iniciantes.md. Badge "MENTALIDADE".
MENTALIDADE_FOREX = [
    # -- Pensar em probabilidades --
    ("Como penso em probabilidades em vez de certezas?", "cada trade é um evento incerto entre muitos; como o cassino, você não sabe a próxima mão, mas confia na matemática ao longo de milhares — o resultado vem da amostra, não do trade"),
    ("Por que 'qualquer coisa pode acontecer' me liberta?", "aceitar que qualquer trade pode dar errado tira o peso de acertar cada um; essa crença é a base para seguir a regra sem medo e sem travar na dúvida"),
    ("Preciso ter razão no trade para ganhar dinheiro?", "não: ter razão é ego, ganhar dinheiro é seguir o processo; buscar estar certo faz segurar perda e realizar lucro cedo — os dois destroem o resultado"),
    ("Como paro de buscar o setup 'perfeito'?", "não existe certeza, existe probabilidade a favor; esperar a confirmação perfeita gera FOMO e entrada atrasada — o plano define 'bom o bastante', não 'perfeito'"),
    # -- Processo acima do resultado --
    ("Como julgo se operei bem num dia de perda?", "pela aderência ao plano, não pelo saldo: seguir a regra e perder é um bom trade; furar a regra e ganhar é um mau trade que você vai repetir"),
    ("Por que focar no processo e não no dinheiro?", "o resultado de um trade é aleatório; o processo é o que você controla e o que se repete — focar no dinheiro traz medo e ganância na pior hora"),
    ("Devo olhar o lucro/prejuízo a cada minuto?", "olhar o saldo o tempo todo transfere a decisão para a emoção; acompanhar o preço pela estrutura, e não pelo dinheiro na tela, mantém a cabeça objetiva"),
    ("Como meço evolução sem ser pelo lucro?", "por disciplina: trades dentro do plano, risco padronizado, erros repetidos caindo; o lucro é consequência de um processo bom mantido numa amostra grande"),
    # -- Aceitar a perda --
    ("Como aceito a perda sem me abalar?", "a perda não é erro, é parte da distribuição da estratégia; aceitá-la ANTES de entrar (imaginar o pior cenário) tira o susto e evita o revenge trade"),
    ("Por que a perda parece um fracasso pessoal?", "porque o ego confunde o resultado do trade com o seu valor; um trade perdido é só informação de um evento probabilístico, não um veredito sobre você"),
    ("Como não levo a perda para o próximo trade?", "encerrando o ciclo: registrar o que aconteceu, aceitar como custo do negócio e voltar ao mesmo processo — carregar a perda é o que gera o revide"),
    ("Estopar e o preço voltar significa que errei?", "não: o stop protegeu o risco planejado; um trade bem executado pode perder, e um mal executado pode ganhar — o certo é ter seguido a regra"),
    # -- Paciência e não operar --
    ("Ficar de fora também é uma decisão?", "sim: não operar quando não há setup protege capital e cabeça ao mesmo tempo; esperar é disciplina ativa, não perda de tempo"),
    ("Como aguento a ansiedade de ficar parado?", "lembrando que o mercado recompensa mais paciência e disciplina do que previsão; a pressa de estar sempre posicionado é o que gera o overtrading"),
    ("Como resisto ao tédio que me faz operar à toa?", "reconhecendo o tédio como gatilho, não como sinal; operar para se sentir ativo força setups ruins — o plano diz quando agir, não a inquietação"),
    # -- Ego, identidade e comparação --
    ("Como separo meu valor pessoal do resultado?", "lembrando que sua autoestima não é o extrato: tratar cada trade como negócio, e não como prova de quem você é, tira o ego da decisão"),
    ("Por que não devo me comparar com outros traders?", "cada um tem capital, tempo e temperamento diferentes; comparar acelera o risco e a pressa — o único parâmetro útil é a sua própria evolução de processo"),
    ("O excesso de confiança depois de acertar é perigoso?", "muito: uma sequência de acertos infla o ego e faz aumentar o risco na hora errada; consistência é humildade repetida, não euforia"),
    ("Como lido com a vontade de 'provar que eu estava certo'?", "abrindo mão dela: insistir numa posição só para ter razão é ego puro; o mercado não deve nada a você, e a regra vale mais que o seu palpite"),
    # -- Hábitos, rotina e disciplina sustentável --
    ("Disciplina é força de vontade?", "não, é hábito: rotina de preparação, regra escrita, tamanho fixo e limite de perda tornam a disciplina automática, sem depender do humor do dia"),
    ("Sono, saúde e rotina afetam meu trade?", "sim: traders consistentes tratam sono, exercício e alimentação como base da disciplina — cabeça cansada decide pior e cede mais à emoção"),
    ("Como registro a emoção, e não só o trade?", "anotando como você se sentiu em cada operação junto do gráfico; rever os estados de cabeça nos altos e baixos revela o padrão que te faz furar a regra"),
    ("Como construo confiança real na minha estratégia?", "por evidência: uma amostra grande seguindo a mesma regra prova o edge; confiança vem de dados repetidos, não de um bom dia isolado"),
    ("Preciso controlar as emoções ou conviver com elas?", "conviver: o objetivo não é não sentir medo ou euforia, é não deixar que decidam por você — a regra fica entre a emoção e o clique"),
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
    cats.append([
        {"key": f"fx:{_slug(nome)}", "fmt": "conceito", "badge": "DÚVIDA DE INICIANTE",
         "nome": nome, "hint": hint}
        for nome, hint in DUVIDAS_FOREX
    ])
    cats.append([
        {"key": f"men:{_slug(nome)}", "fmt": "conceito", "badge": "MENTALIDADE",
         "nome": nome, "hint": hint}
        for nome, hint in MENTALIDADE_FOREX
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
