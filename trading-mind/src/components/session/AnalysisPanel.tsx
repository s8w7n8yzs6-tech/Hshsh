"use client";

import { useState } from "react";
import type { Session, AIAnalysis } from "@/lib/types";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import {
  Sparkles,
  Brain,
  ThumbsUp,
  ThumbsDown,
  ListChecks,
  Dumbbell,
  Quote,
  Radar,
} from "lucide-react";

export function AnalysisPanel({
  session,
  onAnalyzed,
}: {
  session: Session;
  onAnalyzed: (a: AIAnalysis) => void;
}) {
  const [loading, setLoading] = useState(false);
  const analysis = session.analysis;

  const analyze = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ session }),
      });
      const data = await res.json();
      if (data.analysis) onAnalyzed(data.analysis as AIAnalysis);
    } catch {
      // ignore — engine local também roda no server
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="border-brand/20 bg-gradient-to-b from-brand-dim/40 to-card">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-brand to-brand-soft shadow-[0_8px_24px_-8px_rgba(108,62,255,0.8)]">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <h3 className="text-base font-semibold">Psicólogo de Trading IA</h3>
            <p className="text-xs text-muted">Análise focada no processo, não no resultado.</p>
          </div>
        </div>
        <Button onClick={analyze} loading={loading} className="w-full sm:w-auto">
          {!loading && <Sparkles className="h-4 w-4" />}
          {analysis ? "Analisar novamente" : "Analisar Meu Dia"}
        </Button>
      </div>

      {analysis && (
        <div className="mt-6 space-y-5 animate-fade-up">
          {analysis.padroes.length > 0 && (
            <div>
              <div className="mb-2 flex items-center gap-2 text-xs font-medium text-muted">
                <Radar className="h-3.5 w-3.5" /> Padrões detectados
              </div>
              <div className="flex flex-wrap gap-2">
                {analysis.padroes.map((p) => (
                  <Badge key={p} tone="neg">
                    {p}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          <Section icon={<Brain className="h-4 w-4 text-brand-soft" />} title="Resumo psicológico">
            <p className="text-sm leading-relaxed text-ink/90">{analysis.resumo}</p>
          </Section>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <Section icon={<ThumbsUp className="h-4 w-4 text-pos" />} title="Pontos fortes">
              <ul className="space-y-1.5">
                {analysis.pontosFortes.map((x, i) => (
                  <li key={i} className="flex gap-2 text-sm text-ink/90">
                    <span className="mt-1.5 h-1 w-1 flex-none rounded-full bg-pos" />
                    {x}
                  </li>
                ))}
              </ul>
            </Section>
            <Section icon={<ThumbsDown className="h-4 w-4 text-neg" />} title="Pontos fracos">
              <ul className="space-y-1.5">
                {analysis.pontosFracos.map((x, i) => (
                  <li key={i} className="flex gap-2 text-sm text-ink/90">
                    <span className="mt-1.5 h-1 w-1 flex-none rounded-full bg-neg" />
                    {x}
                  </li>
                ))}
              </ul>
            </Section>
          </div>

          <Section icon={<ListChecks className="h-4 w-4 text-brand-soft" />} title="Plano de melhoria">
            <ol className="space-y-2">
              {analysis.planoMelhoria.map((x, i) => (
                <li key={i} className="flex gap-3 text-sm text-ink/90">
                  <span className="flex h-5 w-5 flex-none items-center justify-center rounded-full bg-brand-dim text-[11px] font-semibold text-brand-soft">
                    {i + 1}
                  </span>
                  {x}
                </li>
              ))}
            </ol>
          </Section>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-line2 bg-card2 p-4">
              <div className="mb-2 flex items-center gap-2 text-xs font-medium text-muted">
                <Dumbbell className="h-3.5 w-3.5" /> Exercício mental
              </div>
              <p className="text-sm leading-relaxed text-ink/90">{analysis.exercicioMental}</p>
            </div>
            <div className="flex flex-col justify-center rounded-2xl border border-brand/25 bg-brand-dim p-4">
              <Quote className="h-5 w-5 text-brand-soft" />
              <p className="mt-2 text-sm font-medium leading-relaxed text-ink">
                {analysis.fraseDoDia}
              </p>
            </div>
          </div>

          <p className="text-right text-[11px] text-muted">
            {analysis.fonte === "ia" ? "Gerado por IA" : "Análise inteligente local"} ·{" "}
            {new Date(analysis.geradoEm).toLocaleString("pt-BR")}
          </p>
        </div>
      )}
    </Card>
  );
}

function Section({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted">
        {icon} {title}
      </div>
      {children}
    </div>
  );
}
