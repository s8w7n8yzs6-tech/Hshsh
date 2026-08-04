"use client";

import { cn } from "@/lib/cn";
import { Check } from "lucide-react";

export function Checkbox({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (v: boolean) => void;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={cn(
        "group flex w-full items-center gap-3 rounded-xl border px-3.5 py-3 text-left text-sm transition-all",
        checked
          ? "border-brand/50 bg-brand-dim text-ink"
          : "border-line2 bg-card2 text-muted hover:border-line2 hover:text-ink"
      )}
    >
      <span
        className={cn(
          "flex h-5 w-5 flex-none items-center justify-center rounded-md border transition-all",
          checked ? "border-brand bg-brand" : "border-line2 bg-transparent"
        )}
      >
        {checked && <Check className="h-3.5 w-3.5 text-white" strokeWidth={3} />}
      </span>
      <span className="leading-snug">{label}</span>
    </button>
  );
}

export function Slider({
  label,
  value,
  onChange,
  min = 0,
  max = 100,
  color = "#6C3EFF",
  suffix = "",
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
  min?: number;
  max?: number;
  color?: string;
  suffix?: string;
}) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm text-ink">{label}</span>
        <span className="text-sm font-semibold tabular-nums" style={{ color }}>
          {value}
          {suffix}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="tm-slider h-1.5 w-full cursor-pointer appearance-none rounded-full"
        style={{
          background: `linear-gradient(90deg, ${color} ${pct}%, rgba(255,255,255,0.08) ${pct}%)`,
        }}
      />
      <style jsx>{`
        .tm-slider::-webkit-slider-thumb {
          -webkit-appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 999px;
          background: #fff;
          border: 3px solid ${color};
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
          cursor: pointer;
        }
        .tm-slider::-moz-range-thumb {
          height: 16px;
          width: 16px;
          border-radius: 999px;
          background: #fff;
          border: 3px solid ${color};
          cursor: pointer;
        }
      `}</style>
    </div>
  );
}

export function Toggle({
  checked,
  onChange,
  yesLabel = "Sim",
  noLabel = "Não",
}: {
  checked: boolean | null;
  onChange: (v: boolean) => void;
  yesLabel?: string;
  noLabel?: string;
}) {
  return (
    <div className="inline-flex rounded-xl border border-line2 bg-card2 p-1">
      <button
        type="button"
        onClick={() => onChange(false)}
        className={cn(
          "rounded-lg px-4 py-1.5 text-sm font-medium transition-all",
          checked === false ? "bg-white/10 text-ink" : "text-muted hover:text-ink"
        )}
      >
        {noLabel}
      </button>
      <button
        type="button"
        onClick={() => onChange(true)}
        className={cn(
          "rounded-lg px-4 py-1.5 text-sm font-medium transition-all",
          checked === true ? "bg-neg/20 text-neg" : "text-muted hover:text-ink"
        )}
      >
        {yesLabel}
      </button>
    </div>
  );
}
