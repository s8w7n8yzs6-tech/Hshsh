"use client";

import { useMemo } from "react";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Stat, ProgressRing } from "@/components/ui/Stat";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AreaTrend, EmotionRadar, BarList } from "@/components/charts/Charts";
import {
  computeStats,
  deskProgress,
  buildTimeline,
  computeITP,
  classifyDay,
  DAY_COLORS,
  sessionNet,
  evalAverage,
  BRL,
  num,
  pct,
} from "@/lib/metrics";
import { buildPsychSeries } from "@/lib/psych";
import { exportCSV, exportExcel, exportReportPDF, buildReportHTML } from "@/lib/export";
import type { DayClassification } from "@/lib/types";
import { FileText, Download, FileSpreadsheet, Award, TrendingUp } from "lucide-react";

export default function ReportPage() {
  const { sessions, desk } = useStore();

  const data = useMemo(() => {
    const traded = sessions.filter((s) => s.trades.length > 0);
    const stats = computeStats(sessions);
    const progress = deskProgress(sessions, desk);
    const timeline = buildTimeline(sessions, desk);
    const psych = buildPsychSeries(sessions, 30);

    const sortedByDate = [...traded].sort((a, b) => a.pre.data.localeCompare(b.pre.data));
    const itpValues = sortedByDate.map(computeITP);
    const notaGeral = itpValues.length ? Math.round(itpValues.reduce((a, b) => a + b, 0) / itpValues.length) : 0;

    // maior evolução (ITP início vs fim)
    const half = Math.floor(itpValues.length / 2) || 1;
    const early = itpValues.slice(0, half);
    const late = itpValues.slice(-half);
    const evolucao =
      Math.round((late.reduce((a, b) => a + b, 0) / (late.length || 1))) -
      Math.round((early.reduce((a, b) => a + b, 0) / (early.length || 1)));

    const best = (rec: Record<string, number>) =>
      Object.entries(rec).sort((a, b) => b[1] - a[1])[0];
    const worst = (rec: Record<string, number>) =>
      Object.entries(rec).sort((a, b) => a[1] - b[1])[0];

    const disciplined = [...traded]
      .sort((a, b) => b.selfEval.disciplina - a.selfEval.disciplina)
      .slice(0, 3);
    const impulsive = [...traded]
      .sort((a, b) => (a.selfEval.paciencia + a.selfEval.controleEmocional) - (b.selfEval.paciencia + b.selfEval.controleEmocional))
      .slice(0, 3);

    // erros mais comuns
    const errors: Record<string, number> = {};
    for (const s of traded) {
      if (s.psychology.quisRecuperar) errors["Operar para recuperar perdas"] = (errors["Operar para recuperar perdas"] || 0) + 1;
      if (s.psychology.aumentouLote) errors["Aumentar o lote fora do plano"] = (errors["Aumentar o lote fora do plano"] || 0) + 1;
      if (s.psychology.desobedeceuRegra) errors["Desobedecer regras"] = (errors["Desobedecer regras"] || 0) + 1;
      if (s.psychology.fomo) errors["Entrar por FOMO"] = (errors["Entrar por FOMO"] || 0) + 1;
      if (s.psychology.ansiedade) errors["Operar ansioso"] = (errors["Operar ansioso"] || 0) + 1;
    }
    const mainErrors = Object.entries(errors).sort((a, b) => b[1] - a[1]).slice(0, 4);

    return {
      traded,
      stats,
      progress,
      timeline,
      psych,
      notaGeral,
      evolucao,
      bestAtivo: best(stats.byAtivo),
      bestSetup: best(stats.bySetup),
      bestHour: best(stats.byHour),
      worstHour: worst(stats.byHour),
      disciplined,
      impulsive,
      mainErrors,
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessions, desk]);

  const radar = useMemo(() => {
    const t = data.traded;
    const a = (f: (s: any) => number) => (t.length ? t.reduce((x, s) => x + f(s), 0) / t.length : 0);
    return [
      { axis: "Disciplina", value: a((s) => s.selfEval.disciplina) },
      { axis: "Execução", value: a((s) => s.selfEval.execucao) },
      { axis: "Gestão", value: a((s) => s.selfEval.gestaoRisco) },
      { axis: "Paciência", value: a((s) => s.selfEval.paciencia) },
      { axis: "Emocional", value: a((s) => s.selfEval.controleEmocional) },
    ];
  }, [data.traded]);

  const plan = useMemo(() => buildPlan(data), [data]);
  const strengths = useMemo(() => buildStrengths(data), [data]);
  const weaknesses = data.mainErrors.map(([e, n]) => `${e} (${n}x)`);

  const doPDF = () => {
    const html = buildReportHTML({
      title: "Trading Mind — Relatório dos 30 dias",
      periodo: `${data.traded.length} dias operados · ITP médio ${data.notaGeral}/100`,
      stats: [
        { k: "Lucro total", v: BRL(data.progress.lucroTotal) },
        { k: "Nota geral (ITP)", v: `${data.notaGeral}/100` },
        { k: "Taxa de acerto", v: pct(data.stats.winRate, 1) },
        { k: "Fator de lucro", v: num(isFinite(data.stats.profitFactor) ? data.stats.profitFactor : 0, 2) },
        { k: "Drawdown máximo", v: BRL(data.progress.drawdownMaximo) },
        { k: "Evolução do ITP", v: `${data.evolucao >= 0 ? "+" : ""}${data.evolucao} pts` },
      ],
      strengths,
      weaknesses,
      patterns: weaknesses,
      plan,
      calendar: data.traded,
    });
    exportReportPDF(html);
  };

  return (
    <>
      <PageHeader
        title="Relatório dos 30 dias"
        subtitle="Uma fotografia completa da sua evolução como trader."
        action={
          <div className="flex flex-wrap gap-2">
            <Button onClick={doPDF}>
              <FileText className="h-4 w-4" /> PDF
            </Button>
            <Button variant="ghost" onClick={() => exportExcel(sessions)}>
              <FileSpreadsheet className="h-4 w-4" /> Excel
            </Button>
            <Button variant="ghost" onClick={() => exportCSV(sessions)}>
              <Download className="h-4 w-4" /> CSV
            </Button>
          </div>
        }
      />

      {/* Nota geral + resumo financeiro */}
      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="flex flex-col items-center justify-center gap-3 text-center">
          <ProgressRing value={data.notaGeral} caption="Nota geral" color="#6C3EFF" size={148} />
          <Badge tone={data.evolucao >= 0 ? "pos" : "neg"}>
            <TrendingUp className="h-3.5 w-3.5" /> Evolução {data.evolucao >= 0 ? "+" : ""}{data.evolucao} pts
          </Badge>
          <p className="text-xs text-muted">Índice Trader Profissional médio</p>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader title="Resumo financeiro" subtitle="O resultado é consequência do processo." />
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <MiniStat label="Lucro total" value={BRL(data.progress.lucroTotal)} tone={data.progress.lucroTotal >= 0 ? "pos" : "neg"} />
            <MiniStat label="Taxa de acerto" value={pct(data.stats.winRate, 0)} />
            <MiniStat label="Fator de lucro" value={num(isFinite(data.stats.profitFactor) ? data.stats.profitFactor : 0, 2)} />
            <MiniStat label="Expectância" value={BRL(data.stats.expectancy)} />
            <MiniStat label="Maior gain" value={BRL(data.stats.biggestGain)} tone="pos" />
            <MiniStat label="Maior loss" value={BRL(data.stats.biggestLoss)} tone="neg" />
            <MiniStat label="Drawdown máx." value={BRL(data.progress.drawdownMaximo)} tone="warn" />
            <MiniStat label="Operações" value={String(data.stats.totalTrades)} />
          </div>
        </Card>
      </div>

      {/* Destaques */}
      <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-5">
        <Stat label="Ativo + lucrativo" value={data.bestAtivo?.[0] ?? "—"} sub={data.bestAtivo ? BRL(data.bestAtivo[1]) : ""} tone="pos" />
        <Stat label="Setup + lucrativo" value={data.bestSetup?.[0] ?? "—"} sub={data.bestSetup ? BRL(data.bestSetup[1]) : ""} tone="brand" />
        <Stat label="Melhor horário" value={data.bestHour?.[0] ?? "—"} sub={data.bestHour ? BRL(data.bestHour[1]) : ""} tone="pos" />
        <Stat label="Pior horário" value={data.worstHour?.[0] ?? "—"} sub={data.worstHour ? BRL(data.worstHour[1]) : ""} tone="neg" />
        <Stat label="Dias operados" value={data.progress.diasOperados} icon={<Award className="h-4 w-4" />} />
      </div>

      {/* Timeline + radar */}
      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="Linha do tempo — ITP" subtitle="A curva do seu profissionalismo" />
          <AreaTrend data={data.timeline} dataKey="itp" color="#6C3EFF" yDomain={[0, 100]} />
        </Card>
        <Card>
          <CardHeader title="Radar emocional" subtitle="Médias do período" />
          <EmotionRadar data={radar} height={220} />
        </Card>
      </div>

      {/* Erros e evolução */}
      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Principais erros" subtitle="O que mais atrapalhou seu processo" />
          {data.mainErrors.length ? (
            <ul className="space-y-2.5">
              {data.mainErrors.map(([e, n]) => (
                <li key={e} className="flex items-center justify-between rounded-xl bg-card2 px-3.5 py-2.5">
                  <span className="text-sm">{e}</span>
                  <Badge tone="neg">{n}x</Badge>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-muted">Nenhum erro recorrente registrado. Excelente.</p>
          )}
        </Card>
        <Card>
          <CardHeader title="Evolução do saldo" subtitle="Curva de capital" />
          <AreaTrend data={data.timeline} dataKey="saldo" color="#22C55E" fmt={(v) => `R$${num(v / 1000, 0)}k`} />
        </Card>
      </div>

      {/* Dias disciplinados vs impulsivos */}
      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Dias mais disciplinados" />
          <DayList items={data.disciplined} metric={(s) => `${Math.round(s.selfEval.disciplina)}/100`} tone="pos" />
        </Card>
        <Card>
          <CardHeader title="Dias de maior impulsividade" />
          <DayList items={data.impulsive} metric={(s) => `paciência ${Math.round(s.selfEval.paciencia)}`} tone="neg" />
        </Card>
      </div>

      {/* Calendário 30 dias */}
      <Card className="mb-4">
        <CardHeader title="Calendário dos 30 dias" />
        <div className="flex flex-wrap gap-1.5">
          {data.traded.map((s) => {
            const c = DAY_COLORS[classifyDay(s)];
            return (
              <span
                key={s.id}
                className="h-6 w-6 rounded-md"
                style={{ background: c.bg }}
                title={`${s.pre.data} — ${c.label}`}
              />
            );
          })}
        </div>
      </Card>

      {/* Plano personalizado */}
      <Card className="border-brand/20 bg-gradient-to-b from-brand-dim/30 to-card">
        <CardHeader
          title="Plano personalizado para os próximos 30 dias"
          subtitle="Construído a partir dos seus próprios padrões"
        />
        <ol className="space-y-3">
          {plan.map((p, i) => (
            <li key={i} className="flex gap-3">
              <span className="flex h-6 w-6 flex-none items-center justify-center rounded-full bg-brand text-xs font-semibold text-white">
                {i + 1}
              </span>
              <span className="text-sm leading-relaxed text-ink/90">{p}</span>
            </li>
          ))}
        </ol>
        <div className="mt-5 rounded-xl border border-brand/25 bg-brand-dim p-4 text-center">
          <p className="text-sm font-medium text-ink">Processo acima do resultado. Sempre.</p>
        </div>
      </Card>
    </>
  );
}

function MiniStat({ label, value, tone = "default" }: { label: string; value: string; tone?: string }) {
  const c = { pos: "text-pos", neg: "text-neg", warn: "text-warn", brand: "text-brand-soft", default: "text-ink" }[tone] ?? "text-ink";
  return (
    <div className="rounded-xl bg-card2 px-3 py-2.5">
      <div className="text-[11px] text-muted">{label}</div>
      <div className={`mt-0.5 text-base font-semibold tabular-nums ${c}`}>{value}</div>
    </div>
  );
}

function DayList({
  items,
  metric,
  tone,
}: {
  items: any[];
  metric: (s: any) => string;
  tone: "pos" | "neg";
}) {
  if (!items.length) return <p className="text-sm text-muted">Sem dados suficientes.</p>;
  return (
    <ul className="space-y-2">
      {items.map((s) => (
        <li key={s.id} className="flex items-center justify-between rounded-xl bg-card2 px-3.5 py-2.5">
          <span className="text-sm">
            {new Date(s.pre.data + "T12:00:00").toLocaleDateString("pt-BR", { day: "2-digit", month: "short" })}
            <span className="ml-2 text-xs text-muted">{sessionNet(s) >= 0 ? "+" : ""}{BRL(sessionNet(s))}</span>
          </span>
          <Badge tone={tone}>{metric(s)}</Badge>
        </li>
      ))}
    </ul>
  );
}

function buildStrengths(data: any): string[] {
  const out: string[] = [];
  if (data.stats.winRate >= 50) out.push(`Boa taxa de acerto (${pct(data.stats.winRate, 0)}).`);
  if (data.evolucao > 0) out.push(`Seu ITP evoluiu ${data.evolucao} pontos ao longo do período.`);
  if (data.progress.seqDisciplina >= 3) out.push(`Sequência de ${data.progress.seqDisciplina} dias sem quebra de gerenciamento.`);
  if (data.bestSetup) out.push(`O setup "${data.bestSetup[0]}" é seu mais consistente.`);
  if (out.length === 0) out.push("Consistência no registro do diário — base de todo trader profissional.");
  return out;
}

function buildPlan(data: any): string[] {
  const plan: string[] = [];
  const errs = data.mainErrors.map((e: [string, number]) => e[0]);
  if (errs.includes("Operar para recuperar perdas"))
    plan.push("Instituir limite rígido de 2 stops/dia. Ao atingir, encerrar o pregão imediatamente.");
  if (errs.includes("Aumentar o lote fora do plano"))
    plan.push("Fixar o lote padrão por sessão e só reavaliar tamanho fora do horário de mercado.");
  if (errs.includes("Operar ansioso") || errs.includes("Entrar por FOMO"))
    plan.push("Ritual pré-mercado de 5 minutos de respiração antes de abrir a plataforma.");
  if (data.worstHour)
    plan.push(`Evitar operar no horário ${data.worstHour[0]}, seu período historicamente mais negativo.`);
  if (data.bestHour)
    plan.push(`Concentrar energia no horário ${data.bestHour[0]}, onde seu desempenho é melhor.`);
  plan.push("Rodar a análise da IA ao fim de cada dia e revisar o compromisso na manhã seguinte.");
  plan.push("Meta do mês: elevar o ITP médio, não o lucro. O dinheiro é consequência.");
  return plan;
}
