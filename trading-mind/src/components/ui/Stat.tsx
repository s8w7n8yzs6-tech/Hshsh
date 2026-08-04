import { cn } from "@/lib/cn";
import { Card } from "./Card";

export function Stat({
  label,
  value,
  sub,
  tone = "default",
  icon,
  className,
}: {
  label: string;
  value: React.ReactNode;
  sub?: React.ReactNode;
  tone?: "default" | "pos" | "neg" | "brand" | "warn";
  icon?: React.ReactNode;
  className?: string;
}) {
  const toneColor = {
    default: "text-ink",
    pos: "text-pos",
    neg: "text-neg",
    brand: "text-brand-soft",
    warn: "text-warn",
  }[tone];

  return (
    <Card className={cn("p-4", className)} hover>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-muted">{label}</span>
        {icon && <span className="text-muted/70">{icon}</span>}
      </div>
      <div className={cn("mt-2 text-2xl font-semibold tracking-tight tabular-nums", toneColor)}>
        {value}
      </div>
      {sub && <div className="mt-1 text-xs text-muted">{sub}</div>}
    </Card>
  );
}

export function ProgressRing({
  value,
  size = 132,
  stroke = 10,
  color = "#6C3EFF",
  label,
  caption,
}: {
  value: number; // 0-100
  size?: number;
  stroke?: number;
  color?: string;
  label?: React.ReactNode;
  caption?: React.ReactNode;
}) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const clamped = Math.max(0, Math.min(100, value));
  const offset = c - (clamped / 100) * c;
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeDasharray={c}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.16,1,0.3,1)" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-2xl font-semibold tabular-nums text-ink">{label ?? Math.round(clamped)}</span>
        {caption && <span className="text-[11px] text-muted">{caption}</span>}
      </div>
    </div>
  );
}
