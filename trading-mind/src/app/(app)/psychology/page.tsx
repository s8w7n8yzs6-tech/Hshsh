"use client";

import { useMemo } from "react";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { MultiLine, EmotionRadar } from "@/components/charts/Charts";
import { buildPsychSeries, generateInsights } from "@/lib/psych";
import { Lightbulb, TrendingUp, TrendingDown, AlertTriangle, Sparkles } from "lucide-react";
import { cn } from "@/lib/cn";

const SERIES = [
  { key: "disciplina", name: "Disciplina", color: "#6C3EFF" },
  { key: "confianca", name: "Confiança", color: "#22C55E" },
  { key: "paciencia", name: "Paciência", color: "#38BDF8" },
];
const NEG_SERIES = [
  { key: "ansiedade", name: "Ansiedade", color: "#F5B301" },
  { key: "medo", name: "Medo", color: "#EF4444" },
  { key: "ganancia", name: "Ganância", color: "#F97316" },
  { key: "impulsividade", name: "Impulsividade", color: "#EC4899" },
];

const toneMap = {
  pos: { icon: TrendingUp, cls: "border-pos/25 bg-pos/5 text-pos" },
  neg: { icon: TrendingDown, cls: "border-neg/25 bg-neg/5 text-neg" },
  warn: { icon: AlertTriangle, cls: "border-warn/25 bg-warn/5 text-warn" },
  brand: { icon: Sparkles, cls: "border-brand/25 bg-brand-dim text-brand-soft" },
} as const;

export default function PsychologyPage() {
  const { sessions } = useStore();
  const series = useMemo(() => buildPsychSeries(sessions, 30), [sessions]);
  const insights = useMemo(() => generateInsights(sessions), [sessions]);

  const avg = (k: string) =>
    series.length ? series.reduce((a, p: any) => a + p[k], 0) / series.length : 0;

  const radar = [
    { axis: "Disciplina", value: avg("disciplina") },
    { axis: "Confiança", value: avg("confianca") },
    { axis: "Paciência", value: avg("paciencia") },
    { axis: "Controle", value: 100 - avg("ansiedade") },
    { axis: "Foco", value: 100 - avg("impulsividade") },
  ];

  return (
    <>
      <PageHeader title="Psicológico" subtitle="Últimos 30 dias — a mente por trás dos números." />

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="Fortalezas mentais" subtitle="Disciplina, confiança e paciência ao longo do tempo" />
          <MultiLine data={series} series={SERIES} height={240} />
          <Legend items={SERIES} />
        </Card>
        <Card>
          <CardHeader title="Perfil emocional médio" />
          <EmotionRadar data={radar} color="#22C55E" height={240} />
        </Card>
      </div>

      <Card className="mb-4">
        <CardHeader title="Gatilhos a vigiar" subtitle="Ansiedade, medo, ganância e impulsividade" />
        <MultiLine data={series} series={NEG_SERIES} height={240} />
        <Legend items={NEG_SERIES} />
      </Card>

      <Card>
        <CardHeader
          title="Insights automáticos"
          subtitle="Padrões detectados no seu comportamento"
          action={<Lightbulb className="h-5 w-5 text-warn" />}
        />
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {insights.map((ins, i) => {
            const { icon: Icon, cls } = toneMap[ins.tone];
            return (
              <div key={i} className={cn("flex items-start gap-3 rounded-xl border p-3.5", cls)}>
                <Icon className="mt-0.5 h-4 w-4 flex-none" />
                <p className="text-sm leading-relaxed text-ink/90">{ins.text}</p>
              </div>
            );
          })}
        </div>
      </Card>
    </>
  );
}

function Legend({ items }: { items: { name: string; color: string }[] }) {
  return (
    <div className="mt-3 flex flex-wrap gap-4">
      {items.map((s) => (
        <span key={s.name} className="flex items-center gap-1.5 text-xs text-muted">
          <span className="h-2 w-2 rounded-full" style={{ background: s.color }} />
          {s.name}
        </span>
      ))}
    </div>
  );
}
