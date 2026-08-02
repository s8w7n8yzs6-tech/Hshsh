# Guia passo a passo — publicar no Instagram automaticamente

Este guia leva você do zero até o sistema postando sozinho no seu Instagram.
É a **única parte manual** (feita uma vez); depois tudo roda no automático.

Tempo estimado: 20–30 min. Você vai obter 5 valores e colá-los nos *Secrets* do
GitHub. No fim, opcionalmente, ativa a **renovação automática do token**.

---

## Visão geral dos valores que você vai coletar

| Valor | Onde consegue | Vira o Secret |
|------|----------------|---------------|
| ID da conta Instagram | Graph API Explorer | `INSTAGRAM_USER_ID` |
| Token de longa duração | Graph API Explorer + troca | `INSTAGRAM_ACCESS_TOKEN` |
| Chave do imgbb | api.imgbb.com | `IMGBB_API_KEY` |
| Chave da Anthropic | console.anthropic.com | `ANTHROPIC_API_KEY` |
| (Renovação) App ID e Secret | Meta for Developers | `FB_APP_ID`, `FB_APP_SECRET` |
| (Renovação) Token do GitHub | github.com/settings | `GH_PAT` |

---

## Parte 1 — Preparar a conta do Instagram

O Instagram só permite publicação por API em contas **Profissional** (Business
ou Creator) **vinculadas a uma Página do Facebook**.

1. No app do Instagram: **Menu (☰) → Configurações e privacidade → Tipo de conta
   e ferramentas → Mudar para conta profissional**. Escolha **Business** (ou
   Creator).
2. Crie uma **Página do Facebook** (se não tiver): em facebook.com, menu **Páginas
   → Criar nova Página**. Pode ser simples.
3. Vincule o Instagram à Página: no Instagram, **Configurações → Central de Contas**
   (ou, na Página do Facebook: **Configurações → Contas vinculadas → Instagram**).

Ao final: uma conta IG Business ligada a uma Página do Facebook, ambas na sua conta.

---

## Parte 2 — Criar o app no Meta for Developers

1. Acesse **https://developers.facebook.com/** e faça login com sua conta do
   Facebook. Aceite os termos de desenvolvedor, se pedir.
2. Topo direito: **Meus Apps → Criar aplicativo**.
3. Em **Casos de uso**, escolha **Outro** → **Avançar**.
4. Tipo de app: **Empresa (Business)** → **Avançar**.
5. Dê um nome (ex.: `posts-trade`), confirme o e-mail e **Criar aplicativo**.
6. No painel do app, em **Adicionar produtos**, procure **Instagram** (ou
   **Instagram Graph API**) e clique **Configurar**.
7. Anote, em **Configurações → Básico**:
   - **ID do aplicativo** → será `FB_APP_ID`
   - **Chave secreta do aplicativo** (clique em *Mostrar*) → será `FB_APP_SECRET`

---

## Parte 3 — Gerar o token e descobrir o ID da conta

Usaremos o **Explorador da Graph API**.

1. Abra **https://developers.facebook.com/tools/explorer/**.
2. No canto direito, em **Aplicativo Meta**, selecione o app que você criou.
3. Clique em **Permissões** e adicione (marque) estas permissões:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
   - `business_management`
4. Clique em **Gerar token de acesso** e conclua o pop-up de login/autorização
   (marque a Página e a conta do Instagram quando for perguntado). Isso gera um
   **token de curta duração** — vamos trocá-lo por um de longa duração adiante.
5. **Descobrir o ID da conta do Instagram:** no campo de consulta (ao lado de
   `GET`), digite e envie:
   ```
   me/accounts?fields=instagram_business_account,name
   ```
   Na resposta, encontre o bloco da sua Página e copie
   `instagram_business_account.id` (um número). **Esse é o `INSTAGRAM_USER_ID`.**
   > Se vier vazio, a conta IG não está bem vinculada à Página — revise a Parte 1.

---

## Parte 4 — Trocar por um token de LONGA duração

O token do Explorer dura ~1 hora. Troque por um de ~60 dias.

Cole esta URL no navegador, **substituindo** `FB_APP_ID`, `FB_APP_SECRET` e
`TOKEN_CURTO` (o token gerado na Parte 3):

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=FB_APP_ID&client_secret=FB_APP_SECRET&fb_exchange_token=TOKEN_CURTO
```

A resposta traz `"access_token": "..."`. **Esse valor longo é o
`INSTAGRAM_ACCESS_TOKEN`.**

> Com a **renovação automática** (Parte 7) ativada, esse token se renova sozinho
> antes de expirar — você não precisa repetir isto.

---

## Parte 5 — imgbb e Anthropic

- **imgbb** (hospeda a imagem; a Meta exige URL pública): acesse
  **https://api.imgbb.com/**, clique em **Get API key**, faça login e copie a
  chave → `IMGBB_API_KEY`.
- **Anthropic** (gera o texto): em **https://console.anthropic.com/** →
  **API Keys → Create Key** → copie → `ANTHROPIC_API_KEY`.

---

## Parte 6 — Colar tudo no GitHub

No repositório: **Settings → Secrets and variables → Actions**.

Na aba **Secrets**, clique **New repository secret** e crie um a um:

| Nome do Secret | Valor |
|----------------|-------|
| `ANTHROPIC_API_KEY` | chave da Anthropic |
| `IMGBB_API_KEY` | chave do imgbb |
| `INSTAGRAM_USER_ID` | ID da conta (Parte 3) |
| `INSTAGRAM_ACCESS_TOKEN` | token longo (Parte 4) |

Na aba **Variables**, clique **New repository variable**:

| Nome da Variable | Valor |
|------------------|-------|
| `PLATFORMS` | `instagram` (ou `threads,instagram`) |

**Testar:** aba **Actions → Posts diários sobre trade → Run workflow**, marque
**dry_run = true** para gerar sem publicar e ver se roda. Depois rode com
`dry_run` desmarcado para o primeiro post real. (Localmente: `python -m src.check`
valida as credenciais.)

Pronto: a partir daqui, o agendamento publica **20 posts/dia sozinho**.

---

## Parte 7 — (Opcional, recomendado) Renovação automática do token

O token da Meta expira em ~60 dias. Para não precisar refazer a Parte 4, o
workflow `Renovar token do Instagram` renova sozinho toda semana. Ele precisa de:

1. `FB_APP_ID` e `FB_APP_SECRET` — da Parte 2 (adicione como Secrets).
2. `GH_PAT` — um **Personal Access Token** do GitHub com permissão de **escrita
   em Secrets** deste repositório, para o job gravar o token renovado:
   - **github.com → Settings (do seu perfil) → Developer settings → Personal
     access tokens → Fine-grained tokens → Generate new token**.
   - Em **Repository access**, selecione **Only select repositories** e escolha
     este repositório.
   - Em **Permissions → Repository permissions → Secrets**, defina **Read and
     write**.
   - Gere e copie o token → adicione como Secret **`GH_PAT`**.
3. Ative rodando uma vez: **Actions → Renovar token do Instagram → Run workflow**.

Depois disso, o token se mantém válido indefinidamente, sem intervenção.

---

## Problemas comuns

- **`instagram_business_account` vazio:** conta IG não é Business ou não está
  vinculada à Página. Refaça a Parte 1.
- **Erro de permissão ao publicar:** faltou `instagram_content_publish` ao gerar
  o token. Refaça a Parte 3 marcando todas as permissões.
- **Imagem não publica:** `IMGBB_API_KEY` ausente/inválida — a Meta exige URL
  pública de imagem.
- **Token expirou:** ative a Parte 7, ou refaça a Parte 4.
