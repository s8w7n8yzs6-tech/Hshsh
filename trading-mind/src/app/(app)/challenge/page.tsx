"use client";

import { useMemo } from "react";
import { useRouter } from "next/navigation";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Stat } from "@/components/ui/Stat";
import { classifyDay, DAY_COLORS, sessionNet, BRL } from "@/lib/metrics";
import type { DayClassification } from "@/lib/types";
import { cn } from "@/lib/cn";

interface DayCell {
  date: string;
  day: number;
  cls: DayClassification;
  hasSession: boolean;
  net: number;
  future: boolean;
}

export default function ChallengePage() {
  const { sessions, desk, getSessionByDate } = useStore();
  const router = useRouter();

  const days: DayCell[] = useMemo(() => {
    const start = new Date(desk.inicioDesafio + "T12:00:00");
    const today = new Date();
    today.setHours(12, 0, 0, 0);
    const out: DayCell[] = [];
    for (let i = 0; i < desk.duracaoDesafio; i++) {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      const date = d.toISOString().slice(0, 10);
      const s = getSessionByDate(date);
      out.push({
        date,
        day: i + 1,
        cls: s ? classifyDay(s) : "cinza",
        hasSession: !!s,
        net: s ? sessionNet(s) : 0,
        future: d.getTime() > today.getTime(),
      });
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessions, desk]);

  const counts = useMemo(() => {
    const c: Record<DayClassification, number> = { cinza: 0, verde: 0, amarelo: 0, vermelho: 0, roxo: 0 };
    for (const d of days) if (d.hasSession) c[d.cls]++;
    return c;
  }, [days]);

  const perfect = counts.roxo;
  const disciplined = counts.verde + counts.roxo;
  const breaks = counts.vermelho;

  return (
    <>
      <PageHeader
        title="Desafio 30 Dias"
        subtitle="Cada dia é um voto no trader que você quer se tornar."
      />

      <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4">
        <Stat label="Dias disciplinados" value={disciplined} tone="pos" />
        <Stat label="Execuções perfeitas" value={perfect} tone="brand" />
        <Stat label="Pequenos erros" value={counts.amarelo} tone="warn" />
        <Stat label="Quebras de gerência" value={breaks} tone="neg" />
      </div>

      <Card>
        <CardHeader
          title="Calendário do desafio"
          subtitle="Clique em um dia para abrir o diário completo."
        />
        <div className="grid grid-cols-5 gap-2.5 sm:grid-cols-6 md:grid-cols-10">
          {days.map((d) => {
            const color = DAY_COLORS[d.cls];
            return (
              <button
                key={d.date}
                onClick={() => router.push(`/session?date=${d.date}`)}
                disabled={d.future}
                className={cn(
                  "group relative flex aspect-square flex-col items-center justify-center rounded-xl border text-center transition-all",
                  d.future
                    ? "cursor-not-allowed border-line bg-card2/40 opacity-40"
                    : "border-line2 hover:scale-[1.04] hover:border-white/20"
                )}
                style={{
                  background: d.hasSession
                    ? `linear-gradient(160deg, ${color.bg}22, ${color.bg}0a)`
                    : undefined,
                }}
                title={`${d.date}${d.hasSession ? " · " + BRL(d.net) : ""}`}
              >
                <span className="text-[10px] font-medium text-muted">Dia</span>
                <span className="text-lg font-semibold leading-none">{d.day}</span>
                <span
                  className="mt-1.5 h-1.5 w-1.5 rounded-full"
                  style={{ background: color.bg, boxShadow: d.hasSession ? `0 0 8px ${color.ring}` : "none" }}
                />
              </button>
            );
          })}
        </div>

        {/* Legenda */}
        <div className="mt-6 flex flex-wrap gap-x-5 gap-y-2 border-t border-line pt-4">
          {(Object.keys(DAY_COLORS) as DayClassification[]).map((k) => (
            <span key={k} className="flex items-center gap-2 text-xs text-muted">
              <span className="h-3 w-3 rounded-full" style={{ background: DAY_COLORS[k].bg }} />
              {DAY_COLORS[k].label}
            </span>
          ))}
        </div>
      </Card>
    </>
  );
}
