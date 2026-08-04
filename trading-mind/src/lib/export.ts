import type { Session } from "./types";
import { sessionNet, computeITP, classifyDay, DAY_COLORS } from "./metrics";

function download(filename: string, content: string, mime: string) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

const HEADERS = [
  "Data",
  "Ativo",
  "Direção",
  "Horário",
  "Setup",
  "Lote",
  "Stop",
  "Take",
  "Resultado",
  "Freio",
  "Observações",
];

function rows(sessions: Session[]): (string | number)[][] {
  const out: (string | number)[][] = [];
  for (const s of sessions) {
    for (const t of s.trades) {
      out.push([
        s.pre.data,
        t.ativo,
        t.direcao,
        t.horario,
        t.setup,
        t.lote,
        t.stop ?? "",
        t.take ?? "",
        t.resultado,
        t.brakeOverride ? "override" : "",
        (t.observacoes ?? "").replace(/\n/g, " "),
      ]);
    }
  }
  return out;
}

export function exportCSV(sessions: Session[]) {
  const esc = (v: string | number) => {
    const s = String(v);
    return /[",;\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [HEADERS, ...rows(sessions)].map((r) => r.map(esc).join(";"));
  download("trading-mind-operacoes.csv", "﻿" + lines.join("\n"), "text/csv;charset=utf-8");
}

export function exportExcel(sessions: Session[]) {
  // Excel abre HTML como planilha (.xls) sem dependências externas.
  const cell = (v: string | number) =>
    `<td>${String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;")}</td>`;
  const head = `<tr>${HEADERS.map((h) => `<th>${h}</th>`).join("")}</tr>`;
  const body = rows(sessions).map((r) => `<tr>${r.map(cell).join("")}</tr>`).join("");
  const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel">
<head><meta charset="utf-8"><style>th{background:#6C3EFF;color:#fff;font-weight:bold}td,th{border:1px solid #ccc;padding:4px}</style></head>
<body><table>${head}${body}</table></body></html>`;
  download("trading-mind-operacoes.xls", html, "application/vnd.ms-excel");
}

// Relatório PDF via janela de impressão (o usuário salva como PDF).
export function exportReportPDF(html: string, title = "Trading Mind — Relatório") {
  const w = window.open("", "_blank");
  if (!w) return;
  w.document.write(`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>${title}</title>
<style>
  *{box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
  body{margin:0;padding:40px;background:#fff;color:#111}
  h1{font-size:24px;margin:0 0 4px}
  h2{font-size:15px;margin:28px 0 10px;color:#6C3EFF;border-bottom:2px solid #eee;padding-bottom:6px}
  .muted{color:#666;font-size:12px}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}
  .stat{border:1px solid #eee;border-radius:10px;padding:12px}
  .stat .k{font-size:11px;color:#666}
  .stat .v{font-size:18px;font-weight:600;margin-top:2px}
  table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
  th{background:#f4f2ff;text-align:left;padding:6px;color:#6C3EFF}
  td{border-bottom:1px solid #eee;padding:6px}
  ul{margin:6px 0;padding-left:18px;font-size:13px}
  .cal{display:grid;grid-template-columns:repeat(10,1fr);gap:5px;margin-top:8px}
  .cal span{aspect-ratio:1;border-radius:5px;display:block}
  @media print{body{padding:20px}}
</style></head><body>${html}
<script>window.onload=()=>{setTimeout(()=>window.print(),300)}</script>
</body></html>`);
  w.document.close();
}

export function buildReportHTML(params: {
  title: string;
  periodo: string;
  stats: { k: string; v: string }[];
  strengths: string[];
  weaknesses: string[];
  patterns: string[];
  plan: string[];
  calendar: Session[];
}) {
  const { title, periodo, stats, strengths, weaknesses, patterns, plan, calendar } = params;
  const statHtml = stats
    .map((s) => `<div class="stat"><div class="k">${s.k}</div><div class="v">${s.v}</div></div>`)
    .join("");
  const cal = calendar
    .map((s) => {
      const c = DAY_COLORS[classifyDay(s)];
      return `<span style="background:${c.bg}" title="${s.pre.data}"></span>`;
    })
    .join("");
  const li = (arr: string[]) => (arr.length ? `<ul>${arr.map((x) => `<li>${x}</li>`).join("")}</ul>` : "<p class='muted'>—</p>");

  return `
  <h1>${title}</h1>
  <p class="muted">${periodo} · Processo acima do resultado</p>

  <h2>Resumo</h2>
  <div class="grid">${statHtml}</div>

  <h2>Padrões observados</h2>
  ${patterns.length ? `<p>${patterns.join(" · ")}</p>` : "<p class='muted'>Nenhum padrão de risco recorrente.</p>"}

  <h2>Pontos fortes</h2>
  ${li(strengths)}

  <h2>Pontos a melhorar</h2>
  ${li(weaknesses)}

  <h2>Plano para os próximos 30 dias</h2>
  ${li(plan)}

  <h2>Calendário do desafio</h2>
  <div class="cal">${cal}</div>
  `;
}
