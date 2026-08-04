"use client";

import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  BarChart,
  Bar,
  Cell,
  Line,
  LineChart,
  ReferenceLine,
} from "recharts";

const grid = "rgba(255,255,255,0.05)";

function TooltipBox({ active, payload, label, fmt }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-xl border border-line2 bg-card2 px-3 py-2 text-xs shadow-soft">
      {label !== undefined && <div className="mb-1 font-medium text-muted">{label}</div>}
      {payload.map((p: any, i: number) => (
        <div key={i} className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full" style={{ background: p.color || p.stroke || p.fill }} />
          <span className="text-ink">
            {p.name}: <span className="font-semibold">{fmt ? fmt(p.value) : p.value}</span>
          </span>
        </div>
      ))}
    </div>
  );
}

export function AreaTrend({
  data,
  dataKey,
  color = "#6C3EFF",
  height = 200,
  fmt,
  yDomain,
}: {
  data: any[];
  dataKey: string;
  color?: string;
  height?: number;
  fmt?: (v: number) => string;
  yDomain?: [number | string, number | string];
}) {
  const id = "grad-" + dataKey;
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 6, right: 6, left: -18, bottom: 0 }}>
        <defs>
          <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.35} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
        <XAxis dataKey="label" tickLine={false} axisLine={false} minTickGap={24} />
        <YAxis
          tickLine={false}
          axisLine={false}
          width={48}
          domain={yDomain ?? ["auto", "auto"]}
          tickFormatter={(v) => (fmt ? fmt(v) : v)}
        />
        <Tooltip content={<TooltipBox fmt={fmt} />} cursor={{ stroke: color, strokeOpacity: 0.3 }} />
        <Area
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          strokeWidth={2}
          fill={`url(#${id})`}
          dot={false}
          activeDot={{ r: 4, fill: color, stroke: "#0D0D0D", strokeWidth: 2 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function MultiLine({
  data,
  series,
  height = 220,
}: {
  data: any[];
  series: { key: string; name: string; color: string }[];
  height?: number;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 6, right: 6, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
        <XAxis dataKey="label" tickLine={false} axisLine={false} minTickGap={20} />
        <YAxis tickLine={false} axisLine={false} width={40} domain={[0, 100]} />
        <Tooltip content={<TooltipBox />} />
        {series.map((s) => (
          <Line
            key={s.key}
            type="monotone"
            dataKey={s.key}
            name={s.name}
            stroke={s.color}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 3.5 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

export function EmotionRadar({
  data,
  height = 260,
  color = "#6C3EFF",
}: {
  data: { axis: string; value: number }[];
  height?: number;
  color?: string;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data} outerRadius="72%">
        <PolarGrid stroke="rgba(255,255,255,0.08)" />
        <PolarAngleAxis dataKey="axis" tick={{ fill: "#A0A0A0", fontSize: 11 }} />
        <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
        <Radar dataKey="value" stroke={color} fill={color} fillOpacity={0.28} strokeWidth={2} />
        <Tooltip content={<TooltipBox />} />
      </RadarChart>
    </ResponsiveContainer>
  );
}

export function BarList({
  data,
  height = 240,
  positiveColor = "#22C55E",
  negativeColor = "#EF4444",
  fmt,
}: {
  data: { name: string; value: number }[];
  height?: number;
  positiveColor?: string;
  negativeColor?: string;
  fmt?: (v: number) => string;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 6, right: 8, left: -18, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
        <XAxis dataKey="name" tickLine={false} axisLine={false} interval={0} />
        <YAxis tickLine={false} axisLine={false} width={48} tickFormatter={(v) => (fmt ? fmt(v) : v)} />
        <Tooltip content={<TooltipBox fmt={fmt} />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
        <ReferenceLine y={0} stroke="rgba(255,255,255,0.12)" />
        <Bar dataKey="value" radius={[6, 6, 6, 6]} maxBarSize={40}>
          {data.map((d, i) => (
            <Cell key={i} fill={d.value >= 0 ? positiveColor : negativeColor} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
