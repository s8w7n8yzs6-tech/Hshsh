# Guia passo a passo — publicar no Instagram automaticamente

Fluxo usado: **Instagram API com login do Instagram** (`graph.instagram.com`).
É a única parte manual (feita uma vez); depois tudo roda no automático.

## Valores que você vai coletar

| Valor | Onde consegue | Vira o Secret |
|------|----------------|---------------|
| Token de acesso (longa duração) | Painel do app → Gerar tokens | `INSTAGRAM_ACCESS_TOKEN` |
| user_id do Instagram | `graph.instagram.com/me` | `INSTAGRAM_USER_ID` |
| Chave do imgbb | api.imgbb.com | `IMGBB_API_KEY` |
| Chave da Anthropic | console.anthropic.com | `ANTHROPIC_API_KEY` |
| (Renovação) Token do GitHub | github.com/settings | `GH_PAT` |

---

## Parte 1 — Conta do Instagram profissional
A conta precisa ser **Business ou Creator**. No app do Instagram: **Menu ☰ →
Configurações → Tipo de conta e ferramentas → Mudar para conta profissional**.

## Parte 2 — App no Meta for Developers
Já criado (`claudepostapp`). No painel, o produto **Instagram** está em
**"Configuração da API com login do Instagram"**.

## Parte 3 — Permissões, conta e token

Na página **Configuração da API com login do Instagram**:

**1. Permissões**
- Na seção **"1. Adicionar permissões obrigatórias"**, clique em
  **"Add all required permissions"**.
- Vá no menu esquerdo em **"Permissões e recursos"**, busque e **adicione**:
  - `instagram_business_content_publish`  ← necessária para publicar
  - (confirme que `instagram_business_basic` também está lá)

**2. Dar acesso à sua conta (Testador do Instagram)**
- Abra a aba **Funções** (menu esquerdo → Funções do app → **Funções**).
- Em **Testadores do Instagram**, clique **Adicionar pessoas**, digite o **@ do
  seu Instagram** e envie o convite.
- **Aceite o convite** no app do Instagram: **Configurações → Apps e sites (ou
  "Aplicativos e sites") → Convites de testador → Aceitar**.

**3. Gerar o token**
- Volte para **Configuração da API com login do Instagram → seção "2. Gerar
  tokens de acesso"** → **Adicionar conta**.
- Faça login com a **sua conta do Instagram** e **autorize** todas as permissões.
- O painel vai exibir um **token de acesso** (longa duração, ~60 dias).
  **Copie e guarde** → será o `INSTAGRAM_ACCESS_TOKEN`.
  ⚠️ Token é sigiloso — não cole no chat; vai direto no Secret do GitHub.

**4. Descobrir o user_id**
- Cole no navegador (trocando `SEU_TOKEN`):
  ```
  https://graph.instagram.com/v21.0/me?fields=user_id,username&access_token=SEU_TOKEN
  ```
- A resposta traz `"user_id": "1784...".` **Esse número é o `INSTAGRAM_USER_ID`.**

---

## Parte 4 — imgbb e Anthropic
- **imgbb** (hospeda a imagem; a Meta exige URL pública): **https://api.imgbb.com/**
  → **Get API key** → copie → `IMGBB_API_KEY`.
- **Anthropic** (gera o texto): **https://console.anthropic.com/** → **API Keys →
  Create Key** → copie → `ANTHROPIC_API_KEY`.

---

## Parte 5 — Colar tudo no GitHub
Repositório → **Settings → Secrets and variables → Actions**.

**Secrets** (New repository secret):

| Nome | Valor |
|------|-------|
| `ANTHROPIC_API_KEY` | chave da Anthropic |
| `IMGBB_API_KEY` | chave do imgbb |
| `INSTAGRAM_USER_ID` | user_id (Parte 3.4) |
| `INSTAGRAM_ACCESS_TOKEN` | token (Parte 3.3) |

**Variables** (New repository variable):

| Nome | Valor |
|------|-------|
| `PLATFORMS` | `instagram` |

**Testar:** aba **Actions → Posts diários sobre trade → Run workflow** com
**dry_run = true** (gera sem publicar). Depois, sem o dry_run, para o 1º post real.

Pronto: a partir daqui, publica **20 posts/dia sozinho** (07:00–20:30 BRT).

---

## Parte 6 — (Opcional, recomendado) Renovação automática do token
O token expira em ~60 dias. O workflow **"Renovar token do Instagram"** renova
sozinho toda semana (via `ig_refresh_token`, sem app secret). Ele só precisa de:

1. `GH_PAT` — **Personal Access Token** do GitHub com escrita em **Secrets** deste
   repositório:
   - **github.com → Settings → Developer settings → Personal access tokens →
     Fine-grained tokens → Generate new token**.
   - **Repository access**: *Only select repositories* → este repositório.
   - **Permissions → Repository permissions → Secrets**: **Read and write**.
   - Gere, copie → adicione como Secret **`GH_PAT`**.
2. Ative rodando uma vez: **Actions → Renovar token do Instagram → Run workflow**.

---

## Problemas comuns
- **Não achou `instagram_business_content_publish`:** adicione em **Permissões e
  recursos** (não fica no Explorador da Graph API).
- **"Adicionar conta" não deixa gerar token:** falta aceitar o convite de
  **Testador do Instagram** (Parte 3.2) no app do Instagram.
- **Imagem não publica:** `IMGBB_API_KEY` ausente/inválida — a Meta exige URL
  pública de imagem.
- **Erro de permissão ao publicar:** confirme `instagram_business_content_publish`
  ativa e que o token foi gerado depois de adicioná-la.
