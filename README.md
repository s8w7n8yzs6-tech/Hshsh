# Hshsh — 20 posts diários sobre trade

Gera e publica automaticamente posts sobre trade em **Threads** e **Instagram**.
São **20 posts por dia**, distribuídos das **07:00 às 20:30 (horário de Brasília)**:

- **2 posts de mercado/dia** — 1 de **Ouro (XAU/USD)** e 1 de **Nasdaq**, cada um
  com **gráfico de candlestick de 30 min** e **dados reais** (Yahoo Finance).
- **18 posts focados no trader** — a rotina, as emoções e a realidade de quem
  opera, para o seguidor **se identificar**.

> ⚠️ O conteúdo é **informativo/educacional**. O sistema é instruído a **nunca**
> dar recomendação de compra/venda, alvo de preço ou promessa de lucro — evitando
> configurar aconselhamento financeiro.

## Como funciona

O texto de cada post é escrito pela API da Anthropic (Claude). Para o comentário
de mercado, dados reais de **Ouro (XAU/USD)** e **Nasdaq 100** (Yahoo Finance) são
passados ao modelo como contexto factual.

O agendamento roda via **GitHub Actions** (`.github/workflows/daily-posts.yml`):
há **20 horários por dia** (07:00–20:30 BRT) e **cada execução gera e publica 1
post**. O tipo é decidido pelo horário: os slots das **08:25** (Ouro) e **16:14**
(Nasdaq) são de mercado; todos os outros são de trader. Sem estado entre execuções.

Cada post sai como um **card visual chamativo** em **retrato (1080x1350)**, com:

- **Tema + badge por tipo** (`TRADER` teal, `MERCADO` ciano)
- **Chamada curta e impactante** na imagem + legenda completa no texto do post
- **Gráfico de candlestick (30 min)** só nos 2 posts de mercado (Ouro/Nasdaq)
- **Sua assinatura** (`@thiago.cunhaff`) no rodapé

| Plataforma | Requisito de mídia | Observação |
|-----------|--------------------|------------|
| **Threads** | Aceita imagem via URL pública | Com `IMGBB_API_KEY` publica o card; sem ela, cai para texto |
| **Instagram** | Exige imagem com URL pública | Precisa de `IMGBB_API_KEY` para hospedar o card |

> As imagens são geradas com **Pillow** (card) + **matplotlib** (gráfico) e
> hospedadas no **imgbb** (URL pública exigida pelas APIs da Meta).

## Configuração

Copie `.env.example` para `.env` e preencha, ou configure como *secrets/variables*
do GitHub Actions.

### Secrets do GitHub (Settings → Secrets and variables → Actions → Secrets)
- `ANTHROPIC_API_KEY`
- `THREADS_USER_ID`, `THREADS_ACCESS_TOKEN`
- `INSTAGRAM_USER_ID`, `INSTAGRAM_ACCESS_TOKEN` (só se usar Instagram)
- `IMGBB_API_KEY` (só se usar Instagram — chave grátis em https://api.imgbb.com/)

### Variables do GitHub (mesma tela → Variables)
- `PLATFORMS` — ex.: `threads` ou `threads,instagram`
- `ANTHROPIC_MODEL` — padrão `claude-sonnet-5` (use `claude-haiku-4-5` para custo mínimo)
- `POST_LANGUAGE` — ex.: `português do Brasil` (padrão)
- `POST_HANDLE` — @ acrescentado ao final de cada post (padrão `@thiago.cunhaff`)

> O conteúdo é sempre gerado em português por padrão, e cada post termina com o @
> configurado como assinatura. Ambos têm valores-padrão embutidos, então funcionam
> mesmo sem definir as variables no GitHub.

> 📄 **Passo a passo completo do Instagram:** veja [`SETUP_INSTAGRAM.md`](SETUP_INSTAGRAM.md)
> — cobre criar o app Meta, gerar o token, achar o ID da conta e a **renovação
> automática do token** (o token da Meta expira em ~60 dias; um workflow o renova
> sozinho toda semana).

### Como obter as credenciais Meta
- **Threads**: crie um app no [Meta for Developers](https://developers.facebook.com/),
  adicione a Threads API, conecte a conta Threads e gere um token de longa duração.
  `THREADS_USER_ID` é o ID da sua conta Threads.
- **Instagram**: conta **Business/Creator** conectada a uma Página do Facebook; use
  a Instagram Graph API para obter `INSTAGRAM_USER_ID` e o token de acesso.

> Tokens da Meta expiram — troque por tokens de longa duração e renove periodicamente.

## Testar localmente

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Só gerar, sem publicar (salva um preview.png):
python -m src.post --dry-run

# Forçar um tipo específico:
python -m src.post --type mercado --dry-run

# Verificar credenciais (Instagram/Threads/imgbb) sem publicar nada:
python -m src.check
```

## Estrutura

```
src/
  config.py            # lê variáveis de ambiente
  market.py            # dados reais de Ouro (XAU/USD) e Nasdaq 100 (Yahoo Finance)
  chart.py             # gráfico de candlestick 30min (matplotlib) para posts de mercado
  theme.py             # cores/badges por tipo de conteúdo
  generate.py          # escreve a chamada + a legenda via Claude
  image.py             # monta o card visual 1080x1350 (retrato)
  image_host.py        # hospeda a imagem no imgbb (URL pública)
  post.py              # orquestra: gera 1 post e publica
  check.py             # valida credenciais (Instagram/Threads/imgbb)
  publishers/
    threads.py         # publica no Threads
    instagram.py       # publica no Instagram
.github/workflows/daily-posts.yml   # agendamento (20x/dia) + disparo manual
```

## Ajustes comuns

- **Horários dos posts**: as 20 linhas `cron` em `daily-posts.yml` (em UTC) e a
  lista `SCHEDULE_BRT` em `src/config.py` (em horário de Brasília). Mantenha as
  duas em sincronia se mudar os horários.
- **Quais slots são de mercado**: `GOLD_SLOT_INDEX` / `NASDAQ_SLOT_INDEX` em
  `src/config.py`.
- **Custo**: 20 posts/dia são chamadas curtas; `claude-haiku-4-5` é a opção mais
  barata. O raciocínio estendido já vem desativado em `generate.py`.

## Limitações e responsabilidade

- 20 posts/dia é volume alto — respeite os limites e políticas de cada plataforma
  para não ter a conta sinalizada.
- Revise o conteúdo periodicamente; conteúdo financeiro automatizado pode ter
  implicações legais dependendo do país/regulação.
