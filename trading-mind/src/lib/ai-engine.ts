import type { Session, AIAnalysis } from "./types";
import {
  detectPatterns,
  sessionNet,
  evalAverage,
  computeITP,
  emotionalLoad,
} from "./metrics";

// Motor de análise psicológica local (determinístico) — sempre disponível,
// mesmo sem chave de IA. Foca no PROCESSO, nunca no resultado financeiro.
export function analyzeLocally(s: Session): AIAnalysis {
  const patterns = detectPatterns(s).filter((p) => p.present);
  const net = sessionNet(s);
  const itp = computeITP(s);
  const load = emotionalLoad(s);
  const media = evalAverage(s.selfEval);
  const p = s.psychology;

  // ── Resumo ──────────────────────────────────────────────
  let resumo = "";
  if (patterns.length === 0 && media >= 80) {
    resumo =
      "Seu dia demonstra maturidade emocional e aderência ao processo. Você respeitou seu plano, manteve o gerenciamento e não deixou o resultado financeiro ditar suas decisões. Este é exatamente o comportamento de um trader profissional em construção — repetir esse padrão é o que constrói consistência.";
  } else if (patterns.some((x) => x.key === "revenge")) {
    resumo =
      "Identifiquei sinais claros de revenge trade: após perdas, você tentou recuperar aumentando exposição. Esse é o comportamento que mais destrói contas — não pelo prejuízo de hoje, mas pelo hábito que ele reforça. O ponto central não é o dinheiro perdido, e sim a decisão de operar a partir da dor. Trabalhar esse gatilho é sua maior alavanca de evolução agora.";
  } else if (load >= 50) {
    resumo =
      "Seu estado emocional pesou nas decisões de hoje. Vários gatilhos (ansiedade, medo ou pressa) estiveram presentes, e isso tende a reduzir a qualidade da execução independente do resultado. A boa notícia: você registrou e reconheceu — o primeiro passo do controle é a consciência.";
  } else {
    resumo =
      "Foi um dia intermediário. Houve acertos no processo, mas também pequenos desvios que valem atenção. Lembre-se: o objetivo não é um dia perfeito, e sim a tendência de melhora. Ajustes pequenos e consistentes valem mais que grandes viradas emocionais.";
  }

  // ── Pontos fortes ──────────────────────────────────────
  const pontosFortes: string[] = [];
  if (s.pre.checklist.seguindoPlano) pontosFortes.push("Entrou no mercado com plano definido.");
  if (!p.aumentouLote) pontosFortes.push("Manteve o lote — gerenciamento preservado.");
  if (!p.desobedeceuRegra) pontosFortes.push("Respeitou as próprias regras.");
  if (s.selfEval.paciencia >= 75) pontosFortes.push("Boa paciência para esperar os setups.");
  if (s.selfEval.controleEmocional >= 75) pontosFortes.push("Controle emocional acima da média.");
  if (s.pre.checklist.aceitaStop) pontosFortes.push("Aceitou o stop antes de operar — mentalidade de risco saudável.");
  if (pontosFortes.length === 0) pontosFortes.push("Registrou o dia com honestidade — autoconhecimento é o começo da evolução.");

  // ── Pontos fracos ──────────────────────────────────────
  const pontosFracos: string[] = [];
  if (p.quisRecuperar) pontosFracos.push("Operou com o desejo de recuperar perdas.");
  if (p.aumentouLote) pontosFracos.push("Aumentou o lote fora do plano de gerenciamento.");
  if (p.desobedeceuRegra) pontosFracos.push(`Desobedeceu uma regra${p.qualRegra ? `: ${p.qualRegra}` : "."}`);
  if (p.fomo) pontosFracos.push("Sentiu FOMO — entrou por medo de perder o movimento.");
  if (p.ansiedade) pontosFracos.push("Ansiedade presente durante as operações.");
  if (patterns.some((x) => x.key === "overtrade")) pontosFracos.push("Excesso de operações (overtrade).");
  if (pontosFracos.length === 0) pontosFracos.push("Nenhum desvio grave — refine detalhes de execução.");

  // ── Plano de melhoria ──────────────────────────────────
  const planoMelhoria: string[] = [];
  if (patterns.some((x) => x.key === "revenge") || p.quisRecuperar)
    planoMelhoria.push("Defina um limite rígido de 2 stops. Ao atingir, encerre o dia — sem exceções.");
  if (p.aumentouLote)
    planoMelhoria.push("Fixe o lote por sessão. Só reavalie o tamanho fora do horário de mercado.");
  if (p.ansiedade || p.fomo)
    planoMelhoria.push("Antes de cada entrada, respire 3 vezes e confirme: 'É setup ou é impulso?'");
  if (patterns.some((x) => x.key === "overtrade"))
    planoMelhoria.push("Limite o número de operações por dia. Qualidade acima de quantidade.");
  if (planoMelhoria.length === 0)
    planoMelhoria.push("Continue o processo atual e documente o que funcionou para replicar.");
  planoMelhoria.push("Releia amanhã de manhã seu compromisso: consciência antes do pregão.");

  // ── Exercício mental ───────────────────────────────────
  const exercicios = [
    "Antes do próximo pregão, escreva em uma frase: 'Meu trabalho hoje é executar bem, não ganhar dinheiro.' Leia em voz alta.",
    "Faça 5 minutos de respiração 4-7-8 antes de abrir a plataforma. Só comece quando a mente estiver em ritmo neutro.",
    "Visualize por 2 minutos você tomando um stop com calma e seguindo em frente. Ensaie a calma antes de precisar dela.",
    "Ao sentir vontade de recuperar, feche a plataforma por 10 minutos. O mercado estará lá; sua conta talvez não.",
  ];
  const exercicioMental = patterns.some((x) => x.key === "revenge")
    ? exercicios[3]
    : load >= 50
    ? exercicios[1]
    : exercicios[Math.floor((itp / 100) * (exercicios.length - 1))];

  // ── Frase do dia ───────────────────────────────────────
  const frases = [
    "Processo acima do resultado. Sempre.",
    "Disciplina é escolher o que você quer a longo prazo em vez do que quer agora.",
    "Um trade não define você. Seus hábitos, sim.",
    "O mercado paga pela paciência, não pela pressa.",
    "Perder seguindo o plano é vitória. Ganhar quebrando o plano é derrota disfarçada.",
    "Você não precisa recuperar nada. Precisa apenas executar bem o próximo setup.",
  ];
  const fraseDoDia = patterns.some((x) => x.key === "revenge")
    ? frases[5]
    : frases[Math.abs(hashDate(s.pre.data)) % frases.length];

  return {
    resumo,
    pontosFortes,
    pontosFracos,
    planoMelhoria,
    exercicioMental,
    fraseDoDia,
    padroes: patterns.map((p) => p.label),
    geradoEm: new Date().toISOString(),
    fonte: "local",
  };
}

function hashDate(d: string): number {
  let h = 0;
  for (let i = 0; i < d.length; i++) h = (h * 31 + d.charCodeAt(i)) | 0;
  return h;
}

// Monta o prompt do "psicólogo de trading" para a IA (Anthropic).
export function buildPsychPrompt(s: Session): string {
  const net = sessionNet(s);
  const patterns = detectPatterns(s).filter((p) => p.present).map((p) => p.label);
  return `Você é um PSICÓLOGO ESPECIALISTA EM TRADING. Analise o diário abaixo focando SEMPRE no PROCESSO e no comportamento, NUNCA apenas no resultado financeiro. Nunca incentive o trader a operar mais ou recuperar perdas. Seja acolhedor, direto e técnico.

Responda ESTRITAMENTE em JSON válido com as chaves:
{"resumo": string, "pontosFortes": string[], "pontosFracos": string[], "planoMelhoria": string[], "exercicioMental": string, "fraseDoDia": string, "padroes": string[]}

DADOS DO DIÁRIO:
- Data: ${s.pre.data}
- Sentimento antes: ${s.pre.sentimentoAntes || "—"}
- Checklist pré-mercado: ${JSON.stringify(s.pre.checklist)}
- Nº de operações: ${s.trades.length}
- Resultado líquido (referência, NÃO é o foco): ${net}
- Psicologia: ${JSON.stringify(s.psychology)}
- Autoavaliação (0-100): ${JSON.stringify(s.selfEval)}
- Reflexão: ${JSON.stringify(s.reflection)}
- Padrões detectados por heurística: ${patterns.join(", ") || "nenhum"}

Detecte, quando houver: Revenge Trade, Overtrade, Ganância, Medo, Ansiedade, FOMO, Impulsividade, Quebra de gerenciamento, Excesso de confiança. Preencha "padroes" com os que se aplicam.`;
}
