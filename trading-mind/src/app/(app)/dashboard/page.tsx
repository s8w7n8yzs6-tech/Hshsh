"use client";

import Link from "next/link";
import { useMemo } from "react";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Stat, ProgressRing } from "@/components/ui/Stat";
import { Badge } from "@/components/ui/Badge";
import { AreaTrend } from "@/components/charts/Charts";
import { deskProgress, buildTimeline, BRL, num } from "@/lib/metrics";
import {
  Wallet,
  Target,
  TrendingUp,
  TrendingDown,
  CalendarCheck,
  Flame,
  ShieldCheck,
  Plus,
  Trophy,
  ArrowUpRight,
} from "lucide-react";

export default function DashboardPage() {
  const { sessions, desk } = useStore();
  const progress = useMemo(() => deskProgress(sessions, desk), [sessions, desk]);
  const timeline = useMemo(() => buildTimeline(sessions, desk), [sessions, desk]);

  const approvalPct = Math.min(
    100,
    Math.max(0, (progress.lucroTotal / Math.max(1, desk.metaMesa)) * 100)
  );

  const hasData = timeline.length > 0;

  return (
    <>
      <PageHeader
        title="Dashboard"
        subtitle="Seu progresso no processo — não apenas no resultado."
        action={
          <Link href="/session" className="btn-primary">
            <Plus className="h-4 w-4" strokeWidth={2.5} />
            Nova Sessão
          </Link>
        }
      />

      {/* Aprovação / ITP hero */}
      <div className="mb-5 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2 flex flex-col justify-between gap-6 sm:flex-row sm:items-center">
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-muted">Progresso de aprovação</span>
              {progress.aprovado && <Badge tone="pos">Aprovado</Badge>}
            </div>
            <div className="mt-2 flex items-end gap-2">
              <span className="text-3xl font-semibold tracking-tight">{BRL(progress.lucroTotal)}</span>
              <span className="mb-1 text-sm text-muted">/ {BRL(desk.metaMesa)}</span>
            </div>
            <p className="mt-1 text-xs text-muted">
              {progress.faltaAprovacao > 0
                ? `Faltam ${BRL(progress.faltaAprovacao)} para aprovação`
                : "Meta da mesa atingida — mantenha a disciplina."}
            </p>
            <div className="mt-4 h-2.5 w-full overflow-hidden rounded-full bg-card2">
              <div
                className="h-full rounded-full bg-gradient-to-r from-brand to-brand-soft transition-all duration-700"
                style={{ width: `${approvalPct}%` }}
              />
            </div>
            <div className="mt-4 flex flex-wrap gap-4 text-xs text-muted">
              <span className="flex items-center gap-1.5">
                <CalendarCheck className="h-3.5 w-3.5" /> {progress.diasOperados} dias operados
              </span>
              <span className="flex items-center gap-1.5">
                <Target className="h-3.5 w-3.5" /> {progress.diasRestantes} dias restantes
              </span>
            </div>
          </div>

          <div className="flex flex-col items-center gap-2">
            <ProgressRing value={progress.itpMedio} caption="ITP médio" color="#6C3EFF" />
            <Badge tone="brand">Índice Trader Profissional</Badge>
          </div>
        </Card>

        <div className="grid grid-cols-2 gap-4">
          <Stat
            label="Sequência positiva"
            value={progress.seqDiasPositivos}
            sub="dias no verde"
            tone="pos"
            icon={<Flame className="h-4 w-4" />}
          />
          <Stat
            label="Sequência disciplina"
            value={progress.seqDisciplina}
            sub="dias sem quebra"
            tone="brand"
            icon={<ShieldCheck className="h-4 w-4" />}
          />
          <Stat label="Drawdown atual" value={BRL(progress.drawdownAtual)} tone="warn" icon={<TrendingDown className="h-4 w-4" />} />
          <Stat label="Drawdown máx." value={BRL(progress.drawdownMaximo)} tone="neg" icon={<TrendingDown className="h-4 w-4" />} />
        </div>
      </div>

      {/* KPI grid */}
      <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <Stat label="Saldo atual" value={BRL(progress.saldoAtual)} icon={<Wallet className="h-4 w-4" />} />
        <Stat label="Meta da mesa" value={BRL(desk.metaMesa)} icon={<Target className="h-4 w-4" />} />
        <Stat
          label="Lucro total"
          value={BRL(progress.lucroTotal)}
          tone={progress.lucroTotal >= 0 ? "pos" : "neg"}
          icon={<TrendingUp className="h-4 w-4" />}
        />
        <Stat label="Meta de lucro / dia" value={BRL(desk.metaLucroDia)} icon={<Target className="h-4 w-4" />} />
        <Stat label="Dias operados" value={progress.diasOperados} icon={<CalendarCheck className="h-4 w-4" />} />
        <Stat label="Dias restantes" value={progress.diasRestantes} icon={<CalendarCheck className="h-4 w-4" />} />
      </div>

      {/* Charts */}
      {hasData ? (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader title="Evolução do saldo" subtitle="Curva de capital ao longo do desafio" />
            <AreaTrend data={timeline} dataKey="saldo" color="#6C3EFF" fmt={(v) => `R$${num(v / 1000, 0)}k`} />
          </Card>
          <Card>
            <CardHeader title="Evolução do ITP" subtitle="Índice Trader Profissional por dia" />
            <AreaTrend data={timeline} dataKey="itp" color="#22C55E" yDomain={[0, 100]} />
          </Card>
          <Card>
            <CardHeader title="Evolução da disciplina" subtitle="Sua nota de disciplina diária" />
            <AreaTrend data={timeline} dataKey="disciplina" color="#8A63FF" yDomain={[0, 100]} />
          </Card>
          <Card>
            <CardHeader title="Evolução emocional" subtitle="Estabilidade emocional (maior é melhor)" />
            <AreaTrend data={timeline} dataKey="emocional" color="#F5B301" yDomain={[0, 100]} />
          </Card>
        </div>
      ) : (
        <EmptyState />
      )}
    </>
  );
}

function EmptyState() {
  return (
    <Card className="flex flex-col items-center justify-center gap-4 py-16 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-dim">
        <Trophy className="h-6 w-6 text-brand-soft" />
      </div>
      <div>
        <h3 className="text-base font-semibold">Comece seu diário</h3>
        <p className="mx-auto mt-1 max-w-xs text-sm text-muted">
          Registre sua primeira sessão para acompanhar sua evolução emocional e de disciplina.
        </p>
      </div>
      <Link href="/session" className="btn-primary">
        Nova Sessão <ArrowUpRight className="h-4 w-4" />
      </Link>
    </Card>
  );
}
