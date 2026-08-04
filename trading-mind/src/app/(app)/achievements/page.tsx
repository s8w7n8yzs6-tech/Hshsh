"use client";

import { useMemo } from "react";
import { useStore } from "@/lib/store";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { computeAchievements } from "@/lib/achievements";
import { cn } from "@/lib/cn";
import {
  Lock,
  Award,
  Sparkles,
  ShieldCheck,
  Target,
  BarChart3,
  Gem,
  Flame,
  Crown,
} from "lucide-react";

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  Sparkles,
  ShieldCheck,
  Target,
  BarChart3,
  Gem,
  Lock,
  Flame,
  Crown,
  Award,
};

export default function AchievementsPage() {
  const { sessions } = useStore();
  const achievements = useMemo(() => computeAchievements(sessions), [sessions]);
  const unlocked = achievements.filter((a) => a.unlocked).length;

  return (
    <>
      <PageHeader
        title="Conquistas"
        subtitle="Recompensas pelo processo — não pelo lucro."
        action={<Badge tone="brand">{unlocked} / {achievements.length} desbloqueadas</Badge>}
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {achievements.map((a) => {
          const Icon = ICONS[a.icon] ?? Award;
          return (
            <Card
              key={a.id}
              className={cn(
                "relative overflow-hidden transition-all",
                a.unlocked ? "border-brand/30" : "opacity-90"
              )}
            >
              {a.unlocked && (
                <div className="pointer-events-none absolute -right-8 -top-8 h-24 w-24 rounded-full bg-brand/20 blur-2xl" />
              )}
              <div className="flex items-start gap-3">
                <div
                  className={cn(
                    "flex h-12 w-12 flex-none items-center justify-center rounded-2xl",
                    a.unlocked
                      ? "bg-gradient-to-br from-brand to-brand-soft text-white shadow-[0_8px_24px_-8px_rgba(108,62,255,0.8)]"
                      : "bg-card2 text-muted"
                  )}
                >
                  {a.unlocked ? <Icon className="h-6 w-6" /> : <Lock className="h-5 w-5" />}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-semibold">{a.title}</h3>
                    {a.unlocked && <Badge tone="pos">✓</Badge>}
                  </div>
                  <p className="mt-0.5 text-xs text-muted">{a.description}</p>
                </div>
              </div>

              <div className="mt-4">
                <div className="mb-1.5 flex items-center justify-between text-xs">
                  <span className="text-muted">Progresso</span>
                  <span className="font-medium text-ink tabular-nums">
                    {Math.min(a.current, a.target)} / {a.target}
                  </span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-card2">
                  <div
                    className={cn(
                      "h-full rounded-full transition-all duration-700",
                      a.unlocked ? "bg-pos" : "bg-brand/70"
                    )}
                    style={{ width: `${a.progress * 100}%` }}
                  />
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </>
  );
}
