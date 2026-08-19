"""Personagens conhecidos do mercado financeiro (global e brasileiro).

Cada pessoa vira um CARROSSEL contando a trajetória e as lições dela. O `hint`
resume o motivo da fama, para orientar o modelo e reduzir invenção. O conteúdo
deve ser factual e respeitoso — sem citações inventadas nem recomendação.
"""
from __future__ import annotations

PEOPLE = [
    # --- Global ---
    ("Warren Buffett", "o maior nome do investimento em valor, à frente da Berkshire Hathaway; conhecido pela paciência e pelo foco no longo prazo"),
    ("Charlie Munger", "sócio de Warren Buffett na Berkshire; conhecido pelos modelos mentais e pela racionalidade"),
    ("Benjamin Graham", "o 'pai do value investing', autor de O Investidor Inteligente e mentor de Buffett"),
    ("Peter Lynch", "gestor do fundo Magellan na Fidelity; defensor de investir no que você entende"),
    ("Ray Dalio", "fundador da Bridgewater, maior fundo hedge do mundo; conhecido pelos princípios e pela diversificação"),
    ("George Soros", "megaespeculador que ficou famoso por apostas macroeconômicas históricas"),
    ("Jesse Livermore", "lendário especulador do início do século XX, história de grandes altos e baixos"),
    ("Paul Tudor Jones", "trader macro famoso pela gestão de risco rígida"),
    ("Stanley Druckenmiller", "um dos maiores gestores macro, ex-braço direito de Soros"),
    ("John Bogle", "criador do fundo de índice (Vanguard) e do investimento passivo de baixo custo"),
    ("Jim Simons", "matemático que fundou a Renaissance e o trading quantitativo moderno"),
    ("Michael Burry", "investidor que enxergou a crise de 2008 antes da maioria"),
    ("Nassim Taleb", "autor de A Lógica do Cisne Negro; especialista em risco e incerteza"),
    ("Howard Marks", "fundador da Oaktree, conhecido pelos memorandos sobre ciclos de mercado"),
    ("Carl Icahn", "investidor ativista famoso por pressionar empresas por mudanças"),
    ("Bill Ackman", "gestor ativista conhecido por grandes apostas concentradas"),
    ("David Tepper", "gestor de fundos conhecido por comprar no auge do pessimismo"),
    ("Richard Dennis", "criador do experimento dos 'Turtle Traders', que ensinou traders do zero"),
    ("Ed Seykota", "pioneiro dos sistemas automatizados de trend following"),
    ("Jack Bogle", "defensor incansável do investidor comum e dos custos baixos"),
    # --- Brasil ---
    ("Luiz Barsi Filho", "o maior investidor pessoa física da bolsa brasileira, conhecido pela estratégia de dividendos"),
    ("Lírio Parisotto", "empresário e investidor de valor brasileiro, um dos maiores da B3"),
    ("Luis Stuhlberger", "gestor do fundo Verde, referência histórica da gestão brasileira"),
    ("André Esteves", "fundador do banco BTG Pactual"),
    ("Guilherme Benchimol", "fundador da XP Investimentos, que popularizou a bolsa no Brasil"),
    ("Florian Bartunek", "fundador da Constellation, gestor de valor brasileiro"),
    ("Rogério Xavier", "fundador da SPX Capital, referência em gestão macro no Brasil"),
    ("Márcio Appel", "gestor macro brasileiro, fundador da Adam Capital"),
    ("Luiz Alves Paes de Barros", "investidor discreto e lendário da bolsa brasileira"),
    ("Meireles (José Carlos)", "investidor brasileiro conhecido pela filosofia de longo prazo"),
    ("Pedro Damasceno", "sócio-gestor da Dynamo, uma das gestoras mais respeitadas do Brasil"),
    ("Fabio Alperowitch", "fundador da FAMA Investimentos, referência em investimento de valor e governança"),
]


def slug(nome: str) -> str:
    import re
    import unicodedata

    t = unicodedata.normalize("NFKD", nome.lower()).encode("ascii", "ignore").decode()
    return "-".join(re.findall(r"[a-z0-9]+", t)[:3]) or "x"
