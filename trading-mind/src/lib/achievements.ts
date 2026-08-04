import type { Session } from "./types";
import {
  classifyDay,
  detectRevengeTrade,
  computeStats,
  sessionNet,
} from "./metrics";

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string; // lucide icon name
  progress: number; // 0..1
  current: number;
  target: number;
  unlocked: boolean;
}

function consecutive<T>(arr: T[], pred: (x: T) => boolean): number {
  let best = 0,
    cur = 0;
  for (const x of arr) {
    if (pred(x)) {
      cur++;
      best = Math.max(best, cur);
    } else cur = 0;
  }
  return best;
}

export function computeAchievements(sessions: Session[]): Achievement[] {
  const sorted = [...sessions]
    .filter((s) => s.trades.length > 0)
    .sort((a, b) => a.pre.data.localeCompare(b.pre.data));
  const stats = computeStats(sessions);

  const perfectDays = sorted.filter((s) => classifyDay(s) === "roxo").length;
  const disciplinedStreak = consecutive(sorted, (s) => classifyDay(s) !== "vermelho");
  const noRevengeStreak = consecutive(sorted, (s) => !detectRevengeTrade(s));
  const noLoteIncreaseStreak = consecutive(sorted, (s) => s.psychology.aumentouLote !== true);
  const planStreak = consecutive(sorted, (s) => s.pre.checklist.seguindoPlano && !s.psychology.desobedeceuRegra);
  const perfectTrades = sorted
    .flatMap((s) => (classifyDay(s) === "roxo" ? s.trades : []))
    .length;

  const firstPerfectWeek = consecutive(sorted, (s) => classifyDay(s) === "roxo" || classifyDay(s) === "verde") >= 5;

  const def = (
    id: string,
    title: string,
    description: string,
    icon: string,
    current: number,
    target: number
  ): Achievement => ({
    id,
    title,
    description,
    icon,
    current,
    target,
    progress: Math.max(0, Math.min(1, current / target)),
    unlocked: current >= target,
  });

  return [
    { ...def("first-perfect-week", "Primeira Semana Perfeita", "5 dias seguidos disciplinados", "Sparkles", firstPerfectWeek ? 5 : consecutive(sorted, (s) => classifyDay(s) === "roxo" || classifyDay(s) === "verde"), 5) },
    def("no-revenge-7", "7 Dias Sem Revenge Trade", "Uma semana sem operar para recuperar", "ShieldCheck", noRevengeStreak, 7),
    def("plan-30", "30 Dias Seguindo o Plano", "Um mês de fidelidade ao processo", "Target", planStreak, 30),
    def("trades-100", "100 Operações", "Volume registrado no diário", "BarChart3", stats.totalTrades, 100),
    def("perfect-50", "50 Operações Perfeitas", "Meio-cento de execuções impecáveis", "Gem", perfectTrades, 50),
    def("no-lote-30", "30 Dias Sem Aumentar Lote", "Gerenciamento inabalável", "Lock", noLoteIncreaseStreak, 30),
    def("discipline-10", "10 Dias Seguidos de Disciplina", "Consistência acima de tudo", "Flame", disciplinedStreak, 10),
    def("perfect-days-5", "5 Dias de Execução Perfeita", "Dias roxos no calendário", "Crown", perfectDays, 5),
  ];
}
