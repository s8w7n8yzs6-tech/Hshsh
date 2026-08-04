import type { Session } from "./types";
import { sessionNet, computeStats } from "./metrics";

const clamp = (n: number) => Math.max(0, Math.min(100, Math.round(n)));

export interface PsychPoint {
  date: string;
  label: string;
  disciplina: number;
  confianca: number;
  ansiedade: number;
  ganancia: number;
  medo: number;
  paciencia: number;
  impulsividade: number;
}

// Deriva séries emocionais 0-100 por dia (últimos N dias operados).
export function buildPsychSeries(sessions: Session[], days = 30): PsychPoint[] {
  const sorted = [...sessions]
    .filter((s) => s.trades.length > 0)
    .sort((a, b) => a.pre.data.localeCompare(b.pre.data))
    .slice(-days);

  return sorted.map((s) => {
    const e = s.selfEval;
    const p = s.psychology;
    const d = new Date(s.pre.data + "T12:00:00");
    const flag = (b: boolean | null, base: number) => (b === true ? base : 0);
    return {
      date: s.pre.data,
      label: isNaN(d.getTime())
        ? s.pre.data
        : d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }),
      disciplina: clamp(e.disciplina),
      confianca: clamp(e.execucao * 0.5 + e.controleEmocional * 0.5 - (p.ganancia ? 15 : 0)),
      ansiedade: clamp(flag(p.ansiedade, 55) + (100 - e.controleEmocional) * 0.4 + (p.fomo ? 15 : 0)),
      ganancia: clamp(flag(p.ganancia, 60) + (p.aumentouLote ? 30 : 0) + (100 - e.gestaoRisco) * 0.2),
      medo: clamp(flag(p.medo, 55) + (100 - e.controleEmocional) * 0.3),
      paciencia: clamp(e.paciencia),
      impulsividade: clamp(
        flag(p.aumentouLote, 45) + flag(p.quisRecuperar, 25) + (100 - e.paciencia) * 0.4
      ),
    };
  });
}

export interface Insight {
  text: string;
  tone: "pos" | "neg" | "warn" | "brand";
}

// Gera insights automáticos a partir dos dados reais (com fallback educativo).
export function generateInsights(sessions: Session[]): Insight[] {
  const traded = [...sessions]
    .filter((s) => s.trades.length > 0)
    .sort((a, b) => a.pre.data.localeCompare(b.pre.data));
  const insights: Insight[] = [];
  if (traded.length < 2) {
    return [
      { text: "Registre mais dias para desbloquear insights personalizados sobre seus padrões.", tone: "brand" },
    ];
  }

  // 1. Disciplina após stops consecutivos
  const afterLossDisc: number[] = [];
  const normalDisc: number[] = [];
  for (const s of traded) {
    let consec = 0;
    let hadTwo = false;
    for (const t of s.trades) {
      if (t.resultado < 0) {
        consec++;
        if (consec >= 2) hadTwo = true;
      } else consec = 0;
    }
    (hadTwo ? afterLossDisc : normalDisc).push(s.selfEval.disciplina);
  }
  if (afterLossDisc.length && normalDisc.length) {
    const a = avg(afterLossDisc);
    const b = avg(normalDisc);
    if (b - a >= 8)
      insights.push({
        text: `Você perde disciplina após dois stops consecutivos (média cai de ${Math.round(b)} para ${Math.round(a)}).`,
        tone: "neg",
      });
  }

  // 2. Recuperação de perdas → pior processo
  const recover = traded.filter((s) => s.psychology.quisRecuperar);
  const noRecover = traded.filter((s) => !s.psychology.quisRecuperar);
  if (recover.length && noRecover.length) {
    const rNet = avg(recover.map(sessionNet));
    const nNet = avg(noRecover.map(sessionNet));
    if (nNet - rNet > 0)
      insights.push({
        text: "Você opera pior quando tenta recuperar perdas — seu resultado médio cai nesses dias.",
        tone: "neg",
      });
  }

  // 3. Melhor horário
  const stats = computeStats(sessions);
  const bestHour = Object.entries(stats.byHour).sort((a, b) => b[1] - a[1])[0];
  if (bestHour && bestHour[1] > 0) {
    insights.push({
      text: `Seu melhor horário é por volta das ${bestHour[0].replace("h", "")}:00 — é quando você mais acumula resultado positivo.`,
      tone: "pos",
    });
  }

  // 4. Ansiedade baixa → melhor desempenho
  const calm = traded.filter((s) => !s.psychology.ansiedade);
  const anxious = traded.filter((s) => s.psychology.ansiedade);
  if (calm.length && anxious.length) {
    const cAvg = avg(calm.map((s) => s.selfEval.execucao));
    const aAvg = avg(anxious.map((s) => s.selfEval.execucao));
    if (cAvg - aAvg >= 6)
      insights.push({
        text: "Seu desempenho melhora quando sua ansiedade está baixa. Estado emocional calmo = execução mais limpa.",
        tone: "brand",
      });
  }

  // 5. Aumento de lote
  const loteDays = traded.filter((s) => s.psychology.aumentouLote).length;
  if (loteDays >= 2)
    insights.push({
      text: `Em ${loteDays} dias você aumentou o lote fora do plano. Esse é um gatilho de quebra de gerenciamento a vigiar.`,
      tone: "warn",
    });

  if (insights.length === 0)
    insights.push({
      text: "Seus padrões estão saudáveis. Continue documentando para manter a consistência do processo.",
      tone: "pos",
    });

  return insights;
}

function avg(a: number[]) {
  return a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0;
}
