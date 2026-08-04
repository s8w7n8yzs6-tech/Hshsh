import { cn } from "@/lib/cn";

type Tone = "brand" | "pos" | "neg" | "warn" | "muted";

const tones: Record<Tone, string> = {
  brand: "bg-brand-dim text-brand-soft border-brand/30",
  pos: "bg-pos/10 text-pos border-pos/25",
  neg: "bg-neg/10 text-neg border-neg/25",
  warn: "bg-warn/10 text-warn border-warn/25",
  muted: "bg-card2 text-muted border-line2",
};

export function Badge({
  tone = "muted",
  children,
  className,
}: {
  tone?: Tone;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        tones[tone],
        className
      )}
    >
      {children}
    </span>
  );
}
