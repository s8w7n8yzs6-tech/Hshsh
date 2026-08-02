# Hshsh — 20 posts diários sobre trade

Gera e publica automaticamente posts sobre trade em **Threads** e **Instagram**,
com três tipos de conteúdo:

- **Motivacional / engajamento** — mentalidade, disciplina, gestão de risco.
- **Comentário de mercado** — baseado em **dados reais** (preços de cripto via CoinGecko).
- **Educacional** — conceitos de trade explicados de forma simples.

> ⚠️ O conteúdo é **informativo/educacional**. O sistema é instruído a **nunca**
> dar recomendação de compra/venda, alvo de preço ou promessa de lucro — evitando
> configurar aconselhamento financeiro.

## Como funciona

O texto de cada post é escrito pela API da Anthropic (Claude). Para o comentário
de mercado, dados reais do CoinGecko são passados ao modelo como contexto factual.

O agendamento roda via **GitHub Actions**: o workflow dispara **20 vezes por dia**
(uma por hora, ver `.github/workflows/daily-posts.yml`), e **cada execução gera e
publica 1 post** — resultando em **20 posts/dia**, espaçados ao longo do dia. Sem
estado entre execuções.

| Plataforma | Requisito de mídia | Observação |
|-----------|--------------------|------------|
| **Threads** | Texto puro OK | Funciona só com token de acesso |
| **Instagram** | Exige imagem com URL pública | Geramos a imagem (Pillow) e hospedamos no imgbb |

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
- `POST_LANGUAGE` — ex.: `português do Brasil`

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

# Só gerar, sem publicar:
python -m src.post --dry-run

# Forçar um tipo específico:
python -m src.post --type mercado --dry-run
```

## Estrutura

```
src/
  config.py            # lê variáveis de ambiente
  market.py            # dados reais de cripto (CoinGecko)
  generate.py          # escreve o post via Claude
  image.py             # renderiza o texto em imagem 1080x1080 (Instagram)
  image_host.py        # hospeda a imagem no imgbb (URL pública)
  post.py              # orquestra: gera 1 post e publica
  publishers/
    threads.py         # publica no Threads
    instagram.py       # publica no Instagram
.github/workflows/daily-posts.yml   # agendamento (20x/dia) + disparo manual
```

## Ajustes comuns

- **Quantidade/horário**: edite o `cron` em `daily-posts.yml`. A linha atual
  (`0 9-23,0-4 * * *`) dá exatamente 20 execuções/dia.
- **Proporção dos tipos**: `CONTENT_WEIGHTS` em `src/config.py`.
- **Custo**: 20 posts/dia são chamadas curtas; `claude-haiku-4-5` é a opção mais
  barata. O raciocínio estendido já vem desativado em `generate.py`.

## Limitações e responsabilidade

- 20 posts/dia é volume alto — respeite os limites e políticas de cada plataforma
  para não ter a conta sinalizada.
- Revise o conteúdo periodicamente; conteúdo financeiro automatizado pode ter
  implicações legais dependendo do país/regulação.
