"use client";

import { useMemo } from "react";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Stat } from "@/components/ui/Stat";
import { Button } from "@/components/ui/Button";
import { BarList } from "@/components/charts/Charts";
import { computeStats, BRL, pct, num } from "@/lib/metrics";
import { exportCSV, exportExcel } from "@/lib/export";
import { Download, FileSpreadsheet, Percent, Scale, Trophy, Flame } from "lucide-react";

function toBars(rec: Record<string, number>, limit = 8) {
  return Object.entries(rec)
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
    .slice(0, limit)
    .map(([name, value]) => ({ name, value: Math.round(value) }));
}

const WD_ORDER = ["Seg", "Ter", "Qua", "Qui", "Sex"];

export default function StatisticsPage() {
  const { sessions } = useStore();
  const stats = useMemo(() => computeStats(sessions), [sessions]);

  const fmtR = (v: number) => `R$${num(v, 0)}`;
  const infty = (v: number) => (isFinite(v) ? v : 0);

  const weekdayBars = WD_ORDER.filter((d) => d in stats.byWeekday).map((d) => ({
    name: d,
    value: Math.round(stats.byWeekday[d]),
  }));
  const hourBars = Object.entries(stats.byHour)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([name, value]) => ({ name, value: Math.round(value) }));

  return (
    <>
      <PageHeader
        title="Estatísticas"
        subtitle="Os números do seu processo."
        action={
          <div className="flex gap-2">
            <Button variant="ghost" onClick={() => exportCSV(sessions)}>
              <Download className="h-4 w-4" /> CSV
            </Button>
            <Button variant="ghost" onClick={() => exportExcel(sessions)}>
              <FileSpreadsheet className="h-4 w-4" /> Excel
            </Button>
          </div>
        }
      />

      <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <Stat label="Taxa de acerto" value={pct(stats.winRate, 1)} tone="brand" icon={<Percent className="h-4 w-4" />} />
        <Stat label="Expectância" value={BRL(stats.expectancy)} tone={stats.expectancy >= 0 ? "pos" : "neg"} />
        <Stat label="Payoff" value={num(infty(stats.payoff), 2)} icon={<Scale className="h-4 w-4" />} />
        <Stat label="Fator de lucro" value={num(infty(stats.profitFactor), 2)} tone={stats.profitFactor >= 1 ? "pos" : "neg"} />
        <Stat label="Lucro médio" value={BRL(stats.avgGain)} tone="pos" />
        <Stat label="Loss médio" value={BRL(-stats.avgLoss)} tone="neg" />
      </div>

      <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <Stat label="Operações" value={stats.totalTrades} />
        <Stat label="Gains" value={stats.gains} tone="pos" />
        <Stat label="Losses" value={stats.losses} tone="neg" />
        <Stat label="Maior gain" value={BRL(stats.biggestGain)} tone="pos" icon={<Trophy className="h-4 w-4" />} />
        <Stat label="Maior loss" value={BRL(stats.biggestLoss)} tone="neg" />
        <Stat
          label="Sequências"
          value={`${stats.maxWinStreak} / ${stats.maxLossStreak}`}
          sub="positiva / negativa"
          icon={<Flame className="h-4 w-4" />}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Lucro por ativo" />
          <BarList data={toBars(stats.byAtivo)} fmt={fmtR} />
        </Card>
        <Card>
          <CardHeader title="Lucro por setup" />
          <BarList data={toBars(stats.bySetup)} fmt={fmtR} />
        </Card>
        <Card>
          <CardHeader title="Lucro por horário" />
          <BarList data={hourBars} fmt={fmtR} />
        </Card>
        <Card>
          <CardHeader title="Lucro por dia da semana" />
          <BarList data={weekdayBars} fmt={fmtR} />
        </Card>
      </div>
    </>
  );
}
