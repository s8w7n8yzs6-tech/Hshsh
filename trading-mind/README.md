# Trading Mind

> **Processo acima do resultado.**

Diário de trading com IA para desenvolver **disciplina, consistência e inteligência emocional**. O objetivo não é mostrar lucro e prejuízo — é transformar um trader emocional em um trader profissional.

Interface premium, escura e minimalista (inspirada em Apple, Linear, Notion, TradingView e Raycast), construída com **Next.js 14 + TypeScript + TailwindCSS + Supabase**.

---

## ✨ Funcionalidades

- **Login premium** — email/senha, Google, cadastro e recuperação de senha (Supabase Auth).
- **Dashboard** — saldo, meta da mesa, progresso de aprovação, drawdown, ITP (Índice Trader Profissional), sequências e gráficos de evolução (saldo, disciplina, emocional, ITP).
- **Nova Sessão (diário em 5 etapas):**
  1. **Pré-mercado** — dados do dia + checklist mental + sentimento.
  2. **Operações** — quantas quiser, com setup, lote, stop, take, resultado, screenshot.
  3. **Psicologia** — gatilhos emocionais (medo, ansiedade, ganância, FOMO…).
  4. **Autoavaliação** — notas 0-100 com **radar chart**.
  5. **Reflexão** — erros, acertos, aprendizados e compromissos.
- **🧠 Psicólogo de Trading IA** — analisa o diário, detecta padrões (revenge trade, overtrade, ganância, medo, ansiedade, FOMO, impulsividade, quebra de gerenciamento, excesso de confiança) e gera resumo psicológico, pontos fortes/fracos, plano de melhoria, exercício mental e frase do dia.
- **🚨 Freio de Emergência** *(diferencial exclusivo)* — antes de cada nova operação, um questionário avalia o risco emocional. Em estado de risco alto, o botão "Registrar Operação" é bloqueado por 30 segundos com uma tela de reflexão. A decisão é registrada.
- **Estatísticas** — taxa de acerto, expectância, payoff, fator de lucro, lucro por ativo/setup/horário/dia da semana, maiores gains/losses, sequências.
- **Página psicológica** — evolução de disciplina, confiança, ansiedade, ganância, medo, paciência e impulsividade nos últimos 30 dias + **insights automáticos**.
- **Desafio 30 dias** — calendário colorido (cinza/verde/amarelo/vermelho/roxo). Clique em um dia para abrir o diário.
- **Conquistas** — gamificação (Semana Perfeita, 7 dias sem Revenge Trade, 100 operações…).
- **Relatório dos 30 dias** — resumo financeiro e psicológico, evolução, erros, melhores ativos/horários/setups, nota geral, radar, calendário e **plano personalizado**.
- **Exportação** — PDF, Excel e CSV.

Toda a interface reforça: **nunca incentivar operar mais nem recuperar perdas.**

---

## 🚀 Rodando localmente

```bash
cd trading-mind
npm install
npm run dev
```

Abra <http://localhost:3000>. O app já funciona em **modo demonstração** — sem backend, os dados ficam no navegador e um histórico realista é gerado automaticamente no primeiro login.

## 🔧 Ativando o backend real (opcional)

Copie `.env.example` para `.env.local` e preencha:

```env
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
ANTHROPIC_API_KEY=...        # ativa a IA real; sem ela, usa o motor local
```

1. Crie um projeto no [Supabase](https://supabase.com).
2. Rode o SQL de `supabase/schema.sql` no editor SQL (cria tabelas, RLS, perfis automáticos e o bucket de storage `screenshots`).
3. Ative o provedor **Google** em Authentication → Providers (para o login Google).

---

## 🎨 Design system

| Token | Cor |
|-------|-----|
| Background | `#0D0D0D` |
| Cards | `#171717` |
| Cards secundários | `#222222` |
| Roxo (marca) | `#6C3EFF` |
| Verde | `#22C55E` |
| Vermelho | `#EF4444` |
| Texto | `#FFFFFF` |
| Texto secundário | `#A0A0A0` |

Fonte **Inter**. Animações suaves, microinterações, bordas arredondadas e sombras discretas.

---

## 🏗️ Stack

- **Next.js 14** (App Router) + **React 18** + **TypeScript**
- **TailwindCSS** — design system
- **Recharts** — gráficos (área, linha, radar, barras)
- **Supabase** — auth, banco (Postgres + RLS), storage
- **Anthropic** — psicólogo de trading por IA
- **lucide-react** — ícones

## 📁 Estrutura

```
trading-mind/
├── src/
│   ├── app/
│   │   ├── (app)/            # área autenticada (dashboard, session, statistics…)
│   │   ├── api/analyze/      # rota da IA (Anthropic + fallback local)
│   │   └── login/
│   ├── components/           # UI primitives, charts, session, AppShell
│   └── lib/                  # types, metrics, store, auth, ai-engine, export…
└── supabase/schema.sql       # schema + RLS + storage
```
