"use client";

import { cn } from "@/lib/cn";
import { Check } from "lucide-react";

export function Stepper({
  steps,
  current,
  onStep,
}: {
  steps: string[];
  current: number;
  onStep: (i: number) => void;
}) {
  return (
    <div className="mb-6 overflow-x-auto">
      <div className="flex min-w-max items-center gap-1">
        {steps.map((label, i) => {
          const done = i < current;
          const active = i === current;
          return (
            <div key={label} className="flex items-center">
              <button
                onClick={() => onStep(i)}
                className={cn(
                  "flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition-all",
                  active
                    ? "bg-brand-dim text-ink"
                    : done
                    ? "text-ink hover:bg-white/5"
                    : "text-muted hover:bg-white/5"
                )}
              >
                <span
                  className={cn(
                    "flex h-6 w-6 flex-none items-center justify-center rounded-full text-xs font-semibold transition-all",
                    active
                      ? "bg-brand text-white"
                      : done
                      ? "bg-pos/20 text-pos"
                      : "bg-card2 text-muted"
                  )}
                >
                  {done ? <Check className="h-3.5 w-3.5" strokeWidth={3} /> : i + 1}
                </span>
                <span className="hidden sm:inline">{label}</span>
              </button>
              {i < steps.length - 1 && (
                <div className={cn("mx-1 h-px w-5", done ? "bg-pos/40" : "bg-line2")} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
