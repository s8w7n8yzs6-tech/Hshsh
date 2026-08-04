import { NextResponse } from "next/server";
import type { Session, AIAnalysis } from "@/lib/types";
import { analyzeLocally, buildPsychPrompt } from "@/lib/ai-engine";

export const runtime = "nodejs";

// POST /api/analyze  — body: { session: Session }
// Usa a IA da Anthropic quando ANTHROPIC_API_KEY está definida; caso contrário
// cai no motor local determinístico (sempre disponível).
export async function POST(req: Request) {
  let session: Session;
  try {
    const body = await req.json();
    session = body.session;
    if (!session) throw new Error("missing session");
  } catch {
    return NextResponse.json({ error: "Payload inválido." }, { status: 400 });
  }

  const key = process.env.ANTHROPIC_API_KEY;
  const local = analyzeLocally(session);

  if (!key) {
    return NextResponse.json({ analysis: local });
  }

  try {
    const model = process.env.ANTHROPIC_MODEL || "claude-sonnet-5";
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model,
        max_tokens: 1400,
        system:
          "Você é um psicólogo especialista em trading. Responda SOMENTE com JSON válido, sem texto extra. Foque no processo, nunca incentive operar mais ou recuperar perdas.",
        messages: [{ role: "user", content: buildPsychPrompt(session) }],
      }),
    });

    if (!res.ok) throw new Error("anthropic " + res.status);
    const data = await res.json();
    const text: string = data?.content?.[0]?.text ?? "";
    const json = JSON.parse(extractJson(text));

    const analysis: AIAnalysis = {
      resumo: json.resumo ?? local.resumo,
      pontosFortes: arr(json.pontosFortes, local.pontosFortes),
      pontosFracos: arr(json.pontosFracos, local.pontosFracos),
      planoMelhoria: arr(json.planoMelhoria, local.planoMelhoria),
      exercicioMental: json.exercicioMental ?? local.exercicioMental,
      fraseDoDia: json.fraseDoDia ?? local.fraseDoDia,
      padroes: arr(json.padroes, local.padroes),
      geradoEm: new Date().toISOString(),
      fonte: "ia",
    };
    return NextResponse.json({ analysis });
  } catch {
    // fallback gracioso
    return NextResponse.json({ analysis: local });
  }
}

function arr(v: unknown, fallback: string[]): string[] {
  return Array.isArray(v) && v.length ? v.map(String) : fallback;
}

function extractJson(text: string): string {
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start >= 0 && end > start) return text.slice(start, end + 1);
  return text;
}
