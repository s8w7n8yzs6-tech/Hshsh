# Mente de Trader — site com IA para day traders

Um site de **uma página** (`index.html`, sem servidor) que funciona como:

- 🧠 **Coach & psicólogo financeiro (IA)** — conversa sobre disciplina, medo,
  ganância, revenge trade, FOMO, overtrading e rotina. Lê o seu diário para
  personalizar as respostas.
- 📓 **Diário de trade** — registra cada operação com **emoção antes/depois**,
  se seguiu o plano e os erros/gatilhos. Editar, apagar, exportar/importar.
- 📊 **Painel** — taxa de acerto, resultado acumulado, fator de lucro,
  expectativa (R), curva de resultado, **resultado por emoção** e
  **plano vs. improviso**.
- 💬 **Check‑in emocional** — antes de operar, avalia estado/sono/pressão e dá
  um veredito de risco (🟢🟡🔴), com histórico de humor.

## Como usar

Abra `site/index.html` no navegador. Pronto — os dados ficam **só no seu
navegador** (localStorage). Nada é enviado a lugar nenhum no modo local.

### Modo local (padrão, sem chave)
O coach responde offline com base em regras + análise do seu diário. Funciona
sem internet e sem custo.

### Ativar o Claude (opcional, respostas mais ricas)
Na aba **IA / Dados**, cole uma `ANTHROPIC_API_KEY`. As chamadas vão **direto do
navegador** para a Anthropic (header `anthropic-dangerous-direct-browser-access`).
A chave fica apenas neste navegador.

> 🔒 Expor uma chave no navegador tem risco — use uma chave dedicada com limite
> de gasto. É pensado para **uso pessoal**. Para muitos usuários, o certo é um
> backend que guarde a chave.

## Publicar (GitHub Pages)

Já existe o workflow `.github/workflows/pages.yml`. Ative uma vez em
**Settings → Pages → Source: "GitHub Actions"**. A cada push em `main` que mude
`site/`, o site é publicado.

## Aviso

Ferramenta **educacional e de apoio comportamental**. Não é recomendação de
compra/venda, alvo de preço nem promessa de lucro. Em caso de sofrimento
intenso, procure um profissional de saúde.
