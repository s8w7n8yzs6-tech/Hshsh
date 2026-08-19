# Pesquisa — as maiores dúvidas de quem já passou do zero no Forex

> **Para quem é este documento.** Não é para quem nunca ouviu falar de Forex.
> É para o **iniciante de segundo estágio**: já entende o que é câmbio, pip,
> lote e alavancagem — mas ainda **trava na execução**, no cálculo do tamanho
> da posição, na consistência e na mecânica do dia a dia. São as dúvidas da
> fase "eu sei a teoria, mas por que ainda não engrena?".
>
> ⚠️ **Natureza do conteúdo:** tudo aqui é **informativo/educacional**. Nada é
> recomendação de compra/venda, alvo de preço, promessa de lucro ou
> aconselhamento financeiro. Forex é alavancado e de alto risco — a maioria das
> contas de varejo perde dinheiro.

Organizado em **11 blocos**, na ordem em que um trader de segundo estágio
costuma esbarrar neles.

---

## Índice

1. [Dimensionamento de posição — o cálculo que trava todo mundo](#1-dimensionamento)
2. [Execução e tipos de ordem](#2-execução)
3. ["Tenho estratégia boa e ainda perco" — consistência](#3-consistência)
4. [Métricas, diário e backtest](#4-métricas)
5. [Sessões, timing e liquidez](#5-sessões)
6. [Notícias e volatilidade](#6-notícias)
7. [Correlação e exposição escondida](#7-correlação)
8. [Custos que corroem o resultado](#8-custos)
9. [Da demo para o real](#9-demo-para-real)
10. [Gestão avançada e psicologia de segundo estágio](#10-gestão-avançada)
11. [Mesa proprietária (prop firm)](#11-prop-firm)
12. [Mentalidade — a batalha com a própria cabeça](#12-mentalidade)

No fim: [as 15 dúvidas mais recorrentes deste nível](#top-15) e as [fontes](#fontes).

---

<a name="1-dimensionamento"></a>
## 1. Dimensionamento de posição — o cálculo que trava todo mundo

**Como calcular o tamanho do lote pelo risco?**
A conta é: **risco em dinheiro ÷ (distância do stop em pips × valor do pip)**.
Exemplo citado: arriscar US$ 100, stop de 50 pips, pip de US$ 10 no lote padrão
→ posição de **0,2 lote**. O stop define o risco; o lote se **ajusta** a ele.

**Como saber quanto vale 1 pip na minha conta?**
Depende do par e do tamanho do lote. Regra prática para a maioria dos pares
cotados em dólar: **~US$ 10/pip no lote padrão**, ~US$ 1 no mini e ~US$ 0,10 no
micro. A calculadora de pip/posição da própria corretora resolve isso.

**Por que arriscar só ~1% se posso arriscar mais?**
Porque 1% mantém **qualquer sequência de perdas sobrevivível**. Arriscar muito
por trade dispara o **risco de ruína** e a pressão emocional que faz você
abandonar o plano. A referência mais citada é arriscar **1–2%** da conta por
operação.

**Risco fixo em % ou em valor fixo?**
Em **%** da conta, o tamanho se ajusta sozinho conforme a banca cresce ou
encolhe. Em **valor fixo** é mais simples, mas não se adapta — o mesmo R$ 200 de
risco pesa diferente numa conta de R$ 2 mil e numa de R$ 20 mil.

**Meu stop "apertado" está me tirando cedo demais?**
Provavelmente. Stop curto reduz a perda por trade, mas aumenta a chance de ser
estopado pelo **ruído normal** do mercado. O stop deve **caber na estrutura do
gráfico** — e o lote se ajusta para o risco continuar pequeno.

---

<a name="2-execução"></a>
## 2. Execução e tipos de ordem

**Buy stop x buy limit — qual a diferença?**
- **Buy limit:** compra **abaixo** do preço atual, esperando um recuo para
  entrar mais barato.
- **Buy stop:** compra **acima** do preço atual, confirmando um rompimento.

Um busca **preço melhor**; o outro busca **confirmação**. (Vale o espelho para
sell limit/sell stop.)

**A mercado ou ordem pendente — quando usar cada uma?**
A **mercado** entra já, no preço atual (útil quando o gatilho é agora, mas paga
o spread cheio e sofre slippage). **Pendente** deixa o preço vir até o seu
nível, evitando perseguir — ao custo de, às vezes, não ser executada.

**Quando mover o stop para o zero a zero (breakeven)?**
Em geral **depois** de o trade andar a favor uma distância razoável, para
proteger de virar perda. Cuidado: mover **cedo demais** te tira no ruído normal,
antes de o movimento se desenvolver.

**Vale a pena realizar parcial?**
Encerrar **parte** no primeiro alvo trava lucro e alivia a pressão; deixar o
**resto correr** (muitas vezes com stop no zero) busca o movimento maior. É uma
troca entre **conforto** e **potencial** — não existe certo único.

**Como funciona o trailing stop na prática?**
O stop **acompanha o preço** a uma distância fixa em pips: numa compra, sobe
junto e nunca desce, ficando sempre X pips abaixo da máxima alcançada. Protege
lucro — mas, se for curto demais, te tira na primeira respirada.

---

<a name="3-consistência"></a>
## 3. "Tenho estratégia boa e ainda perco" — consistência

**Tenho uma estratégia boa, por que ainda perco?**
Na maioria das vezes a falha é **execução, não estratégia**. O padrão clássico:
entrar **antes** de o nível confirmar, **alargar o stop** para não estar errado,
e depois **caçar um segundo trade** para recuperar. Isso destrói uma boa
estratégia.

**O que é overtrading e por que sabota?**
Operar **demais** — por tédio, impaciência ou pela crença de que "mais trades =
mais lucro". Aumenta custo, cansaço de decisão e força setups ruins só para se
sentir ativo. É descrito como um **matador silencioso de conta**.

**Por que meu risco varia de um trade para outro?**
O sinal mais claro de rotina amadora é o **risco variável**: um trade pequeno
por cautela, o próximo grande porque "parece certo". **Padronizar o risco** por
operação é justamente o que produz consistência.

**Quantas operações por dia são saudáveis?**
Não há número mágico, mas **poucas operações alinhadas ao plano** batem muitas
por impulso. Definir um **teto diário** de trades é um freio direto contra o
overtrading.

**Como sei se a estratégia realmente funciona?**
Por uma **amostra grande** de trades seguindo **a mesma regra**, medindo a
expectativa — não por dois ou três resultados recentes. Resultado de curto prazo
é ruído.

---

<a name="4-métricas"></a>
## 4. Métricas, diário e backtest

**O que é expectância (edge) e como medir?**
É o **resultado médio esperado por trade**, combinando **taxa de acerto** e
**payoff** (ganho médio ÷ perda média). Positiva no longo prazo = a estratégia
tem vantagem estatística. É o número que diz se vale a pena repetir o processo.

**Taxa de acerto alta é sempre melhor?**
Não. Dá para **lucrar acertando pouco** se o ganho médio for bem maior que a
perda; e dá para **perder acertando muito** se cada perda for enorme. Acerto sem
payoff engana.

**Por que manter um diário de operações?**
Sem registrar **contexto, tamanho e emoção** de cada trade, não há como achar o
padrão dos seus erros. O journal é o que transforma "operar bastante" em
**evoluir**.

**Como faço backtest sem me enganar?**
Testando **a mesma regra** numa amostra grande, **sem** ajustar os parâmetros até
a curva ficar "perfeita" no passado. Esse ajuste excessivo (**overfitting**) não
se repete ao vivo — é a armadilha nº 1 do backtest caseiro.

**O que é R múltiplo?**
Medir cada resultado em **múltiplos do risco inicial (1R)**: um ganho de 2R
pagou dois riscos; uma perda é −1R. Pensar em R tira o foco do dinheiro e coloca
no **processo**, o que ajuda a manter o tamanho de posição estável.

---

<a name="5-sessões"></a>
## 5. Sessões, timing e liquidez

**Qual é o melhor horário para operar?**
A **sobreposição Londres–Nova York** (aprox. 13:00–17:00 GMT / 10:00–14:00 BRT)
concentra o **maior volume** — mais de metade do fluxo diário passa por essas
duas praças — com spreads mais estreitos e execução melhor.

**Por que o spread alarga em certos horários?**
Em **baixa liquidez** (virada de dia, fim de sessão asiática) e ao redor de
**notícias fortes**, o spread abre. No EUR/USD, por exemplo, ele pode saltar de
~0,5–1 pip para **3–8 pips** nos minutos ao redor de um dado importante.

**O horário muda qual par eu devo acompanhar?**
Sim. Cada sessão movimenta mais certos pares. Operar um par no seu **horário de
maior liquidez** costuma dar spread menor e movimento mais limpo do que
forçá-lo num horário morto.

---

<a name="6-notícias"></a>
## 6. Notícias e volatilidade

**Como uso o calendário econômico?**
Para saber **quando** saem os dados de alto impacto — decisão de juros, inflação
(**CPI/PCE**), emprego (**NFP**), PIB, vendas no varejo — que mexem nas
expectativas de juros e sacodem pares como EUR/USD, GBP/USD e USD/JPY. Serve para
**decidir se opera ou fica de fora** naquele horário.

**Devo operar na hora exata da notícia?**
É o momento de **maior spread, slippage e reversão brusca**. Muitos traders
experientes simplesmente **não operam** no minuto do dado — o risco de execução
supera a "oportunidade".

**Por que fui estopado bem no pavio e o preço voltou?**
Em picos de volatilidade, o preço faz **pavios rápidos** e o spread alarga,
tocando o stop antes de retomar a direção. Não é "perseguição" da corretora — é
**execução em baixa liquidez / notícia**. Stop com folga da estrutura e evitar
horários ruins reduzem isso.

---

<a name="7-correlação"></a>
## 7. Correlação e exposição escondida

**O que é correlação entre pares e por que importa?**
Pares que **andam juntos** (vários com dólar, por exemplo) **somam risco**. Abrir
três posições correlacionadas na mesma direção é quase **triplicar a mesma
aposta** sem perceber.

**Estou diversificando ou dobrando o mesmo risco?**
Abrir vários trades na mesma direção do dólar **não diversifica — concentra**.
Olhar uma **matriz de correlação** antes de dimensionar evita empilhar risco
escondido e exceder, na prática, o seu limite por operação.

---

<a name="8-custos"></a>
## 8. Custos que corroem o resultado

**Por que meu resultado veio pior do que eu esperava?**
Quase sempre por **spread, swap, slippage ou comissão** — os custos que o
iniciante esquece de somar. Cada um parece pequeno por trade, mas vira muito em
quem opera bastante.

**O swap pode comer meu lucro no swing?**
Sim. Manter posição vários dias pode acumular **swap negativo** (rolagem
overnight). Em operações longas, esse custo precisa entrar na conta do resultado
esperado.

---

<a name="9-demo-para-real"></a>
## 9. Da demo para o real

**Por que ganho na demo e perco no real?**
Porque a demo **não tem a pressão emocional** do dinheiro real. Medo e ganância
mudam a **execução** — a técnica é a mesma; o gatilho psicológico, não. Por isso
resultado de demo não se transfere direto.

**Como faço a transição da demo para o real?**
Começando com o **menor tamanho possível** (micro lote) para sentir a emoção com
risco mínimo, e só aumentando **depois** de provar consistência com dinheiro de
verdade.

**Quanto tempo devo ficar na demo?**
Até repetir o **mesmo processo** com resultado estável por uma amostra grande.
Passar cedo demais custa caro; ficar tempo demais **adia** o teste emocional que
só o dinheiro real traz.

---

<a name="10-gestão-avançada"></a>
## 10. Gestão avançada e psicologia de segundo estágio

**O que é risco de ruína?**
A **probabilidade de a conta quebrar** por uma sequência de perdas. Risco alto
por trade a dispara **mesmo com uma estratégia lucrativa** — é por isso que o
tamanho da posição é decisivo, não um detalhe.

**Quando posso aumentar o tamanho da posição?**
Só **depois** de provar consistência por uma amostra grande. Aumentar por
euforia após acertos seguidos é como a maioria **devolve** o lucro que juntou.

**Devo reduzir o risco depois de perder?**
Reduzir o tamanho numa sequência ruim protege **capital e cabeça**. Aumentar para
"recuperar rápido" (dobrar a aposta) é o caminho mais curto para quebrar.

**Como paro de mexer no stop no meio do trade?**
Definindo **stop e alvo antes** de entrar e **não tocando** neles. A regra
escrita tira a decisão do calor do momento — que é exatamente onde a perda
pequena e planejada vira grande e não planejada.

**Como lido com um drawdown (sequência de perdas)?**
Aceitando que **faz parte** de qualquer estratégia. O que importa é o **tamanho**
dele caber no seu risco e você seguir o mesmo processo **sem revidar** o mercado.

**Devo ter só uma estratégia ou várias?**
No início, **dominar uma a fundo** dá mais consistência que pular entre várias.
Trocar de método a cada perda impede qualquer uma de **provar seu valor** numa
amostra decente.

**Que timeframe usar já sabendo o básico?**
O **maior** dá o contexto; o **menor**, a entrada. Alinhar dois tempos
(**top-down**) evita operar contra o cenário principal. Mais tempo gráfico nem
sempre é melhor — clareza vale mais que quantidade de telas.

---

<a name="11-prop-firm"></a>
## 11. Mesa proprietária (prop firm)

**O que é uma mesa proprietária (prop firm)?**
Empresa que **cede capital** para você operar depois de um **teste pago
(challenge)**. Você opera o dinheiro dela seguindo regras e **divide o lucro**. O
objetivo delas é uma coisa só: saber se você **protege o capital**.

**Drawdown estático x trailing — qual a diferença?**
- **Estático:** o limite é medido a partir do **saldo inicial** e não se move
  (ex.: conta de US$ 100 mil quebra ao cair para US$ 90 mil, tenha lucrado ou
  não).
- **Trailing:** o limite **sobe junto** com o lucro e aperta a margem (se a conta
  vai a US$ 110 mil, o piso acompanha).

O **trailing** é descrito como a **regra escondida que mais reprova** quem
passaria tranquilo no alvo de lucro.

**Vale a pena entrar numa prop firm como iniciante?**
Só com **consistência já provada**. As regras — meta de lucro, **perda diária**,
**trailing drawdown**, janelas de notícia, limite de posição, restrição de
overnight/fim de semana — reprovam quem ainda não domina gestão de risco. Boa
parte das reprovações vem justamente das regras **além** do drawdown principal.

---

<a name="12-mentalidade"></a>
## 12. Mentalidade — a batalha com a própria cabeça

> Este é o bloco que separa quem "sabe operar" de quem **consegue** operar. No
> segundo estágio, o inimigo raramente é o gráfico — é a própria cabeça. As
> ideias abaixo bebem muito da escola do **pensar em probabilidades** (ex.:
> _Trading in the Zone_, de Mark Douglas).

### Pensar em probabilidades

**Como penso em probabilidades em vez de certezas?**
Cada trade é **um evento incerto entre muitos**. Como o cassino: a casa não sabe
a próxima mão, mas confia na matemática ao longo de milhares. Seu resultado vem
da **amostra**, não de um trade isolado.

**Por que "qualquer coisa pode acontecer" me liberta?**
Aceitar que **qualquer trade pode dar errado** tira o peso de acertar cada um.
Douglas trata essa crença como o **alicerce** de todo o resto: é ela que permite
seguir a regra sem medo e sem travar na dúvida.

**Preciso "ter razão" no trade para ganhar dinheiro?**
Não. Ter razão é **ego**; ganhar dinheiro é seguir o **processo**. Buscar estar
certo faz você segurar a perda e realizar o lucro cedo — os dois corroem o
resultado.

**Como paro de buscar o setup "perfeito"?**
Não existe certeza, existe **probabilidade a favor**. Esperar a confirmação
perfeita gera FOMO e entrada atrasada. O plano define o que é "**bom o
bastante**" — não "perfeito".

### Processo acima do resultado

**Como julgo se operei bem num dia de perda?**
Pela **aderência ao plano**, não pelo saldo. Seguir a regra e perder é um **bom
trade**; furar a regra e ganhar é um **mau trade** — porque você vai repetir o
mau hábito que "deu certo".

**Por que focar no processo e não no dinheiro?**
O resultado de **um** trade é aleatório; o **processo** é o que você controla e o
que se repete. Focar no dinheiro na tela traz medo e ganância na pior hora.

**Devo acompanhar o lucro/prejuízo a cada minuto?**
Olhar o saldo o tempo todo **transfere a decisão para a emoção**. Acompanhar o
preço pela **estrutura do gráfico**, e não pelo dinheiro flutuando, mantém a
cabeça objetiva.

**Como meço evolução sem ser pelo lucro?**
Por **disciplina**: trades dentro do plano, risco padronizado, erros repetidos
caindo. O lucro é **consequência** de um bom processo mantido numa amostra
grande — avalie-se pela disciplina, não pelo P&L do dia.

### Aceitar a perda

**Como aceito a perda sem me abalar?**
A perda **não é erro** — é parte da distribuição da estratégia. Aceitá-la
**antes** de entrar (visualizar o pior cenário) tira o susto e desarma o revenge
trade.

**Por que a perda parece um fracasso pessoal?**
Porque o **ego** confunde o resultado do trade com o seu valor. Um trade perdido
é só **informação** de um evento probabilístico — não um veredito sobre você.

**Como não levo a perda para o próximo trade?**
**Encerrando o ciclo**: registrar o que aconteceu, aceitar como custo do negócio
e voltar ao mesmo processo. Carregar a perda de um trade para o outro é o que
gera o revide.

**Estopar e o preço voltar significa que errei?**
Não. O stop **protegeu o risco planejado**. Um trade bem executado pode perder, e
um mal executado pode ganhar — o "certo" é ter **seguido a regra**.

### Paciência e não operar

**Ficar de fora também é uma decisão?**
Sim. **Não operar** quando não há setup protege capital **e** cabeça. Esperar é
uma disciplina **ativa**, não tempo perdido.

**Como aguento a ansiedade de ficar parado?**
Lembrando que o mercado recompensa **paciência e disciplina** mais do que
previsão. A urgência de estar sempre posicionado é a raiz do overtrading.

**Como resisto ao tédio que me faz operar à toa?**
Reconhecendo o **tédio como gatilho**, não como sinal. Operar para se sentir
ativo força setups ruins. Quem decide é o **plano**, não a inquietação.

### Ego, identidade e comparação

**Como separo meu valor pessoal do resultado?**
Lembrando que sua autoestima **não é o extrato**. Tratar cada trade como
**negócio**, e não como prova de quem você é, tira o ego da decisão.

**Por que não devo me comparar com outros traders?**
Cada um tem **capital, tempo e temperamento** diferentes. Comparação acelera o
risco e a pressa. O único parâmetro útil é a **sua própria** evolução de
processo.

**O excesso de confiança depois de acertar é perigoso?**
Muito. Uma sequência de acertos infla o ego e faz **aumentar o risco na hora
errada**. Consistência é humildade repetida, não euforia.

**Como lido com a vontade de "provar que eu estava certo"?**
Abrindo mão dela. Insistir numa posição só para ter razão é **ego puro**. O
mercado não te deve nada — e a regra vale mais que o palpite.

### Hábitos, rotina e disciplina sustentável

**Disciplina é força de vontade?**
Não — é **hábito**. Rotina de preparação, regra escrita, tamanho fixo e limite de
perda tornam a disciplina **automática**, sem depender do humor do dia.

**Sono, saúde e rotina afetam meu trade?**
Sim. Traders consistentes tratam **sono, exercício e alimentação** como base da
disciplina: cabeça cansada decide pior e cede mais à emoção.

**Como registro a emoção, e não só o trade?**
Anotando **como você se sentiu** em cada operação, junto do gráfico. Rever os
estados de cabeça nos altos e baixos revela o padrão que te faz **furar a
regra**.

**Como construo confiança real na minha estratégia?**
Por **evidência**: uma amostra grande seguindo a mesma regra prova o edge.
Confiança vem de **dados repetidos**, não de um bom dia isolado.

**Preciso controlar as emoções ou conviver com elas?**
**Conviver.** O objetivo não é deixar de sentir medo ou euforia — é não deixar
que **decidam por você**. A regra fica entre a emoção e o clique.

---

<a name="top-15"></a>
## Resumo — as 15 dúvidas mais recorrentes deste nível

1. Como calcular o tamanho do lote a partir do risco e do stop?
2. Quanto vale 1 pip na minha conta e no meu par?
3. Por que arriscar só 1–2% por operação?
4. Buy stop x buy limit — quando usar cada tipo de ordem?
5. Quando mover o stop para o breakeven e quando realizar parcial?
6. Tenho uma estratégia boa — por que ainda perco?
7. O que é overtrading e por que meu risco varia tanto?
8. O que é expectância/edge e como medir de verdade?
9. Como fazer backtest sem cair em overfitting?
10. Qual o melhor horário e por que o spread alarga?
11. Devo operar na hora da notícia? Como usar o calendário?
12. Correlação: estou diversificando ou dobrando o mesmo risco?
13. Por que ganho na demo e perco no real — e como fazer a transição?
14. O que é risco de ruína e quando posso aumentar o tamanho?
15. Prop firm: drawdown estático x trailing e vale a pena para iniciante?

---

<a name="fontes"></a>
## Fontes

Pesquisa consolidada a partir de materiais educativos de corretoras, mesas
proprietárias e portais de educação financeira (acesso em agosto/2026):

- [Babypips — Position Size Calculator](https://www.babypips.com/tools/position-size-calculator)
- [tastyfx — How to Pick a Position Size in Forex Trading](https://www.tastyfx.com/news/position-sizing-forex/)
- [FOREX.com — Margin and Pip Calculator](https://www.forex.com/en-us/help-and-support/margin-pip-calculator/)
- [CashbackForex — Forex Order Types (Buy/Sell Stop, Limit, Market)](https://www.cashbackforex.com/article/order-types)
- [Babypips — Types of Orders](https://www.babypips.com/learn/forex/types-of-orders)
- [Topstep — Market, Limit, Stop and Trailing Stops](https://www.topstep.com/blog/types-orders-trading-market-limit-stop-trailing-stops)
- [Blueberry Markets — What Is Overtrading and How to Avoid It](https://blueberrymarkets.com/market-analysis/what-is-overtrading-and-how-to-avoid-it/)
- [Daily Price Action — How to Reduce Forex Trading Losses](https://dailypriceaction.com/blog/how-to-reduce-forex-trading-losses/)
- [Admiral Markets — Top Reasons Why Forex Traders Fail](https://admiralmarkets.com/education/articles/trading-psychology/top-reasons-why-forex-traders-fail-and-lose-money)
- [Forex Mentor Pro — Best Trading Routines for Consistency](https://www.forexmentorpro.com/blog/best-trading-routines-for-consistency/)
- [Babypips — Best Times of Day to Trade Forex (Session Overlaps)](https://www.babypips.com/learn/forex/session-overlaps)
- [OANDA — When Is the Best Time for Forex Trading?](https://www.oanda.com/us-en/skills-and-insights/education/trading-asset-classes/forex/when-is-the-best-time-for-forex-trading/)
- [ZAYE Capital Markets — The London–New York Overlap Session](https://zayecapitalmarkets.com/london-new-york-overlap-session-2/)
- [ThinkCapital — Prop Firm Drawdown Rules: Daily vs Max](https://www.thinkcapital.com/prop-firm-drawdown-rules/)
- [For Traders — Prop Trading Rules You Must Know Before a Challenge](https://fortraders.com/blog/prop-trading-rules-you-must-know-before-taking-a-challenge)
- [FundingTraders — Prop Firm Trading Rules Explained for Beginners](https://blog.fundingtraders.com/prop-firm-trading-rules/)
- [Ox Securities — Why Forex Traders Lose Money](https://oxsecurities.com/avoid-these-common-mistakes-why-forex-traders-lose-money/)
- [Trade That Swing — Key Takeaways from "Trading in the Zone" (Mark Douglas)](https://tradethatswing.com/key-takeaways-from-trading-in-the-zone-by-mark-douglas/)
- [LiquidityFinder — Trading in the Zone: Thinking in Probabilities](https://liquidityfinder.com/news/trading-in-the-zone-thinking-in-probabilities-943bf)
- [QuantifiedStrategies — The Correct Mindset in Trading](https://www.quantifiedstrategies.com/a-traders-mindset/)
- [New Trader U — Improving Your Trading Patience and Discipline](https://www.newtraderu.com/2022/10/27/steps-to-improving-your-trading-patience-and-discipline/)
- [Britannica Money — Trading Psychology: How to Develop a Trader Mindset](https://www.britannica.com/money/trading-psychology)
- [Dukascopy — Trading Discipline: Rules and Habits of Disciplined Forex Traders](https://www.dukascopy.com/swiss/english/marketwatch/articles/trading-discipline/)

> As referências numéricas (valor de pip por lote, faixa de 1–2% de risco,
> alargamento de spread em notícia, metas e limites de prop firms) são **valores
> típicos dos materiais consultados** — variam por corretora, par, conta e
> período, e **não** devem ser tratadas como número exato nem como promessa.
