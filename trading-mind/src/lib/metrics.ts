import type {
  Session,
  Trade,
  DayClassification,
  DeskConfig,
  SelfEval,
} from "./types";

export const BRL = (n: number) =>
  n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export const num = (n: number, d = 0) =>
  n.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });

export const pct = (n: number, d = 0) => `${num(n, d)}%`;

// ── Sessão ───────────────────────────────────────────────────
export const sessionNet = (s: Session) =>
  s.trades.reduce((a, t) => a + (Number(t.resultado) || 0), 0);

export const avg = (arr: number[]) =>
  arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;

export const evalAverage = (e: SelfEval) =>
  avg([e.disciplina, e.execucao, e.gestaoRisco, e.paciencia, e.controleEmocional]);

// Emoção "carga negativa" 0-100 (quanto maior, pior o estado emocional)
export function emotionalLoad(s: Session): number {
  const p = s.psychology;
  const flags = [
    p.medo,
    p.ansiedade,
    p.ganancia,
    p.fomo,
    p.quisRecuperar,
    p.aumentouLote,
    p.desobedeceuRegra,
  ].filter((x) => x === true).length;
  const brakeRisk = s.brakeEvents.some((b) => b.riscoAlto) ? 1 : 0;
  return Math.min(100, Math.round(((flags + brakeRisk) / 8) * 100));
}

// Estabilidade emocional (0-100, maior = melhor)
export const emotionalStability = (s: Session) => 100 - emotionalLoad(s);

// ── Índice Trader Profissional (ITP) ─────────────────────────
// Combina disciplina, gerenciamento e controle emocional — nunca resultado $$.
export function computeITP(s: Session): number {
  const e = s.selfEval;
  const disciplineBlock = avg([e.disciplina, e.gestaoRisco, e.paciencia]);
  const emotionBlock = avg([e.controleEmocional, emotionalStability(s)]);
  const executionBlock = e.execucao;

  // Penalidades por comportamentos que quebram o processo
  let penalty = 0;
  const p = s.psychology;
  if (p.quisRecuperar) penalty += 8;
  if (p.aumentouLote) penalty += 10;
  if (p.desobedeceuRegra) penalty += 14;
  if (detectRevengeTrade(s)) penalty += 12;
  if (detectOvertrade(s)) penalty += 8;
  if (s.brakeEvents.some((b) => b.riscoAlto && b.decisao === "continuou")) penalty += 10;

  const raw = disciplineBlock * 0.45 + emotionBlock * 0.35 + executionBlock * 0.2;
  return Math.max(0, Math.min(100, Math.round(raw - penalty)));
}

// ── Detecção de padrões (base para IA e classificação) ───────
export function detectRevengeTrade(s: Session): boolean {
  if (s.psychology.quisRecuperar) {
    // depois de um loss, o lote aumentou?
    for (let i = 1; i < s.trades.length; i++) {
      if (s.trades[i - 1].resultado < 0 && s.trades[i].lote > s.trades[i - 1].lote)
        return true;
    }
  }
  // sequência de losses seguida de lote crescente
  return s.psychology.quisRecuperar === true && s.psychology.aumentouLote === true;
}

export function detectOvertrade(s: Session): boolean {
  // muitas operações + queda de disciplina, ou operar muito após bater meta
  const losses = s.trades.filter((t) => t.resultado < 0).length;
  return s.trades.length >= 8 || (losses >= 4 && s.trades.length >= 6);
}

export function detectGreed(s: Session): boolean {
  return (
    s.psychology.ganancia === true ||
    s.psychology.aumentouLote === true ||
    s.selfEval.gestaoRisco < 40
  );
}

export function detectRuleBreak(s: Session): boolean {
  return s.psychology.desobedeceuRegra === true || s.selfEval.disciplina < 40;
}

export interface DetectedPattern {
  key: string;
  label: string;
  present: boolean;
}

export function detectPatterns(s: Session): DetectedPattern[] {
  const p = s.psychology;
  return [
    { key: "revenge", label: "Revenge Trade", present: detectRevengeTrade(s) },
    { key: "overtrade", label: "Overtrade", present: detectOvertrade(s) },
    { key: "greed", label: "Ganância", present: detectGreed(s) },
    { key: "fear", label: "Medo", present: p.medo === true },
    { key: "anxiety", label: "Ansiedade", present: p.ansiedade === true },
    { key: "fomo", label: "FOMO", present: p.fomo === true },
    {
      key: "impulsive",
      label: "Impulsividade",
      present: p.aumentouLote === true || s.selfEval.paciencia < 40,
    },
    { key: "riskbreak", label: "Quebra de gerenciamento", present: detectRuleBreak(s) },
    {
      key: "overconfidence",
      label: "Excesso de confiança",
      present: p.ganancia === true && sessionNet(s) > 0 && p.aumentouLote === true,
    },
  ];
}

// ── Classificação do dia (calendário do desafio) ─────────────
export function classifyDay(s: Session): DayClassification {
  if (s.trades.length === 0) return "cinza";
  const rulebreak = detectRuleBreak(s) || detectRevengeTrade(s);
  const disc = s.selfEval.disciplina;
  const perfect =
    !rulebreak &&
    disc >= 90 &&
    s.selfEval.gestaoRisco >= 85 &&
    s.selfEval.controleEmocional >= 85 &&
    !s.psychology.desobedeceuRegra;

  if (rulebreak) return "vermelho";
  if (perfect) return "roxo";
  const minorErrors =
    s.psychology.ansiedade === true ||
    s.psychology.fomo === true ||
    s.psychology.medo === true ||
    disc < 75;
  return minorErrors ? "amarelo" : "verde";
}

export const DAY_COLORS: Record<DayClassification, { bg: string; ring: string; label: string }> = {
  cinza: { bg: "#222222", ring: "rgba(255,255,255,0.06)", label: "Sem operação" },
  verde: { bg: "#22C55E", ring: "rgba(34,197,94,0.35)", label: "Dia disciplinado" },
  amarelo: { bg: "#F5B301", ring: "rgba(245,179,1,0.35)", label: "Pequenos erros" },
  vermelho: { bg: "#EF4444", ring: "rgba(239,68,68,0.35)", label: "Quebra de gerenciamento" },
  roxo: { bg: "#6C3EFF", ring: "rgba(108,62,255,0.35)", label: "Execução perfeita" },
};

// ── Estatísticas agregadas ───────────────────────────────────
export interface Stats {
  totalTrades: number;
  gains: number;
  losses: number;
  breakeven: number;
  winRate: number;
  avgGain: number;
  avgLoss: number;
  expectancy: number;
  payoff: number;
  profitFactor: number;
  grossProfit: number;
  grossLoss: number;
  net: number;
  biggestGain: number;
  biggestLoss: number;
  maxWinStreak: number;
  maxLossStreak: number;
  byAtivo: Record<string, number>;
  bySetup: Record<string, number>;
  byHour: Record<string, number>;
  byWeekday: Record<string, number>;
}

const WEEKDAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

export function computeStats(sessions: Session[]): Stats {
  const trades: { t: Trade; date: string }[] = [];
  for (const s of sessions) for (const t of s.trades) trades.push({ t, date: s.pre.data });

  const results = trades.map((x) => x.t.resultado);
  const gains = results.filter((r) => r > 0);
  const losses = results.filter((r) => r < 0);
  const breakeven = results.filter((r) => r === 0).length;

  const grossProfit = gains.reduce((a, b) => a + b, 0);
  const grossLoss = Math.abs(losses.reduce((a, b) => a + b, 0));
  const avgGain = gains.length ? grossProfit / gains.length : 0;
  const avgLoss = losses.length ? grossLoss / losses.length : 0;
  const winRate = results.length ? (gains.length / results.length) * 100 : 0;
  const p = winRate / 100;
  const expectancy = p * avgGain - (1 - p) * avgLoss;
  const payoff = avgLoss ? avgGain / avgLoss : avgGain > 0 ? Infinity : 0;
  const profitFactor = grossLoss ? grossProfit / grossLoss : grossProfit > 0 ? Infinity : 0;

  const groupSum = (key: (x: { t: Trade; date: string }) => string) => {
    const out: Record<string, number> = {};
    for (const x of trades) {
      const k = key(x);
      out[k] = (out[k] || 0) + x.t.resultado;
    }
    return out;
  };

  const byHour = groupSum((x) => (x.t.horario || "—").slice(0, 2) + "h");
  const byWeekday = groupSum((x) => {
    const d = new Date(x.date + "T12:00:00");
    return isNaN(d.getTime()) ? "—" : WEEKDAYS[d.getDay()];
  });

  // streaks
  let maxWin = 0,
    maxLoss = 0,
    curW = 0,
    curL = 0;
  for (const r of results) {
    if (r > 0) {
      curW++;
      curL = 0;
    } else if (r < 0) {
      curL++;
      curW = 0;
    } else {
      curW = 0;
      curL = 0;
    }
    maxWin = Math.max(maxWin, curW);
    maxLoss = Math.max(maxLoss, curL);
  }

  return {
    totalTrades: results.length,
    gains: gains.length,
    losses: losses.length,
    breakeven,
    winRate,
    avgGain,
    avgLoss,
    expectancy,
    payoff,
    profitFactor,
    grossProfit,
    grossLoss,
    net: grossProfit - grossLoss,
    biggestGain: gains.length ? Math.max(...gains) : 0,
    biggestLoss: losses.length ? Math.min(...losses) : 0,
    maxWinStreak: maxWin,
    maxLossStreak: maxLoss,
    byAtivo: groupSum((x) => x.t.ativo || "—"),
    bySetup: groupSum((x) => x.t.setup || "—"),
    byHour,
    byWeekday,
  };
}

// ── Séries temporais para dashboard ──────────────────────────
export interface EquityPoint {
  date: string;
  label: string;
  saldo: number;
  disciplina: number;
  emocional: number;
  itp: number;
  net: number;
}

export function buildTimeline(sessions: Session[], desk: DeskConfig): EquityPoint[] {
  const sorted = [...sessions].sort((a, b) => a.pre.data.localeCompare(b.pre.data));
  let running = desk.saldoInicialMesa;
  return sorted.map((s) => {
    const net = sessionNet(s);
    running += net;
    const d = new Date(s.pre.data + "T12:00:00");
    return {
      date: s.pre.data,
      label: isNaN(d.getTime())
        ? s.pre.data
        : d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }),
      saldo: Math.round(running),
      disciplina: Math.round(s.selfEval.disciplina),
      emocional: emotionalStability(s),
      itp: computeITP(s),
      net: Math.round(net),
    };
  });
}

// ── Painel do desafio / aprovação ────────────────────────────
export interface DeskProgress {
  saldoAtual: number;
  lucroTotal: number;
  faltaAprovacao: number;
  drawdownAtual: number;
  drawdownMaximo: number;
  diasOperados: number;
  diasRestantes: number;
  itpMedio: number;
  seqDiasPositivos: number;
  seqDisciplina: number;
  aprovado: boolean;
}

export function deskProgress(sessions: Session[], desk: DeskConfig): DeskProgress {
  const sorted = [...sessions].sort((a, b) => a.pre.data.localeCompare(b.pre.data));
  let saldo = desk.saldoInicialMesa;
  let peak = saldo;
  let maxDD = 0;
  for (const s of sorted) {
    saldo += sessionNet(s);
    peak = Math.max(peak, saldo);
    maxDD = Math.max(maxDD, peak - saldo);
  }
  const lucroTotal = saldo - desk.saldoInicialMesa;
  const drawdownAtual = peak - saldo;

  const diasOperados = sorted.filter((s) => s.trades.length > 0).length;
  const inicio = new Date(desk.inicioDesafio + "T12:00:00");
  const passados = isNaN(inicio.getTime())
    ? diasOperados
    : Math.floor((Date.now() - inicio.getTime()) / 86400000);
  const diasRestantes = Math.max(0, desk.duracaoDesafio - Math.max(passados, diasOperados));

  // sequência de dias positivos (do fim pro início)
  let seqPos = 0;
  for (let i = sorted.length - 1; i >= 0; i--) {
    if (sorted[i].trades.length === 0) continue;
    if (sessionNet(sorted[i]) > 0) seqPos++;
    else break;
  }
  // sequência de disciplina (dias sem quebra de gerenciamento)
  let seqDisc = 0;
  for (let i = sorted.length - 1; i >= 0; i--) {
    if (sorted[i].trades.length === 0) continue;
    const cls = classifyDay(sorted[i]);
    if (cls === "vermelho") break;
    seqDisc++;
  }

  const itpMedio =
    diasOperados > 0
      ? Math.round(avg(sorted.filter((s) => s.trades.length > 0).map(computeITP)))
      : 0;

  return {
    saldoAtual: Math.round(saldo),
    lucroTotal: Math.round(lucroTotal),
    faltaAprovacao: Math.max(0, Math.round(desk.metaMesa - lucroTotal)),
    drawdownAtual: Math.round(drawdownAtual),
    drawdownMaximo: Math.round(maxDD),
    diasOperados,
    diasRestantes,
    itpMedio,
    seqDiasPositivos: seqPos,
    seqDisciplina: seqDisc,
    aprovado: lucroTotal >= desk.metaMesa && maxDD <= desk.drawdownMaximo,
  };
}
