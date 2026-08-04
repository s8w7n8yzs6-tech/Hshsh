"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useStore } from "@/lib/store";
import { newSession } from "@/lib/defaults";
import type { Session, Trade, BrakeEvent, AIAnalysis } from "@/lib/types";
import { PageHeader } from "@/components/ui/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input, Textarea, Select } from "@/components/ui/Input";
import { Checkbox, Slider, Toggle } from "@/components/ui/Field";
import { Badge } from "@/components/ui/Badge";
import { Stepper } from "@/components/session/Stepper";
import { TradeForm } from "@/components/session/TradeForm";
import { EmergencyBrake } from "@/components/session/EmergencyBrake";
import { AnalysisPanel } from "@/components/session/AnalysisPanel";
import { EmotionRadar } from "@/components/charts/Charts";
import { BRL, sessionNet, evalAverage } from "@/lib/metrics";
import {
  ArrowLeft,
  ArrowRight,
  Plus,
  Trash2,
  TrendingUp,
  TrendingDown,
  Check,
  Save,
} from "lucide-react";

const STEPS = ["Pré-mercado", "Operações", "Psicologia", "Autoavaliação", "Reflexão", "IA"];

export default function SessionPage() {
  return (
    <Suspense fallback={null}>
      <SessionWizard />
    </Suspense>
  );
}

function SessionWizard() {
  const router = useRouter();
  const params = useSearchParams();
  const editId = params.get("id");
  const dateParam = params.get("date");
  const { getSession, getSessionByDate, saveSession } = useStore();

  const [session, setSession] = useState<Session | null>(null);
  const [step, setStep] = useState(0);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (editId) {
      const s = getSession(editId);
      if (s) return setSession(structuredClone(s));
    }
    if (dateParam) {
      const s = getSessionByDate(dateParam);
      if (s) return setSession(structuredClone(s));
      const blank = newSession();
      blank.pre.data = dateParam;
      return setSession(blank);
    }
    setSession(newSession());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editId, dateParam]);

  const update = (patch: Partial<Session>) =>
    setSession((prev) => (prev ? { ...prev, ...patch } : prev));

  const persist = (s: Session) => {
    saveSession(s);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  if (!session) return null;

  const net = sessionNet(session);

  return (
    <>
      <PageHeader
        title={editId ? "Editar sessão" : "Nova sessão"}
        subtitle="Registre seu dia. Processo acima do resultado."
        action={
          <div className="flex items-center gap-3">
            {session.trades.length > 0 && (
              <Badge tone={net >= 0 ? "pos" : "neg"}>
                {net >= 0 ? <TrendingUp className="h-3.5 w-3.5" /> : <TrendingDown className="h-3.5 w-3.5" />}
                {BRL(net)}
              </Badge>
            )}
            <Button variant="ghost" onClick={() => persist(session)}>
              {saved ? <Check className="h-4 w-4 text-pos" /> : <Save className="h-4 w-4" />}
              {saved ? "Salvo" : "Salvar"}
            </Button>
          </div>
        }
      />

      <Stepper steps={STEPS} current={step} onStep={setStep} />

      <div className="animate-fade-up">
        {step === 0 && <StepPreMarket session={session} update={update} />}
        {step === 1 && <StepTrades session={session} update={update} />}
        {step === 2 && <StepPsych session={session} update={update} />}
        {step === 3 && <StepEval session={session} update={update} />}
        {step === 4 && <StepReflection session={session} update={update} />}
        {step === 5 && (
          <AnalysisPanel
            session={session}
            onAnalyzed={(a: AIAnalysis) => {
              const next = { ...session, analysis: a };
              setSession(next);
              persist(next);
            }}
          />
        )}
      </div>

      <div className="mt-6 flex items-center justify-between">
        <Button
          variant="ghost"
          onClick={() => setStep((s) => Math.max(0, s - 1))}
          disabled={step === 0}
        >
          <ArrowLeft className="h-4 w-4" /> Voltar
        </Button>
        {step < STEPS.length - 1 ? (
          <Button onClick={() => setStep((s) => Math.min(STEPS.length - 1, s + 1))}>
            Continuar <ArrowRight className="h-4 w-4" />
          </Button>
        ) : (
          <Button
            onClick={() => {
              persist(session);
              router.push("/dashboard");
            }}
          >
            <Check className="h-4 w-4" /> Concluir diário
          </Button>
        )}
      </div>
    </>
  );
}

// ── Etapa 1 — Pré-mercado ──────────────────────────────────────
function StepPreMarket({
  session,
  update,
}: {
  session: Session;
  update: (p: Partial<Session>) => void;
}) {
  const pre = session.pre;
  const setPre = (patch: Partial<typeof pre>) => update({ pre: { ...pre, ...patch } });
  const setCheck = (k: keyof typeof pre.checklist, v: boolean) =>
    setPre({ checklist: { ...pre.checklist, [k]: v } });

  const checks: [keyof typeof pre.checklist, string][] = [
    ["dormiuBem", "Dormi bem"],
    ["descansado", "Estou descansado"],
    ["seguindoPlano", "Estou seguindo meu plano"],
    ["aceitaStop", "Aceito tomar stop hoje"],
    ["naoPrecisaRecuperar", "Não preciso recuperar perdas"],
    ["tranquilo", "Estou tranquilo emocionalmente"],
    ["naoAnsioso", "Não estou ansioso"],
    ["naoPorNecessidade", "Não estou operando por necessidade financeira"],
  ];

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader title="Dados do dia" />
        <div className="grid grid-cols-2 gap-3">
          <Input label="Data" type="date" value={pre.data} onChange={(e) => setPre({ data: e.target.value })} />
          <Input label="Horário" type="time" value={pre.horario} onChange={(e) => setPre({ horario: e.target.value })} />
          <Input label="Ativo" value={pre.ativo} onChange={(e) => setPre({ ativo: e.target.value })} />
          <Input label="Conta" value={pre.conta} onChange={(e) => setPre({ conta: e.target.value })} placeholder="Conta / corretora" />
          <Input
            label="Saldo inicial (R$)"
            type="number"
            value={pre.saldoInicial}
            onChange={(e) => setPre({ saldoInicial: Number(e.target.value) })}
          />
          <Input label="Mesa" value={pre.mesa} onChange={(e) => setPre({ mesa: e.target.value })} placeholder="Ex.: Alpha 50k" />
        </div>
        <div className="mt-3">
          <Input label="Objetivo do dia" value={pre.objetivoDia} onChange={(e) => setPre({ objetivoDia: e.target.value })} placeholder="Ex.: seguir o plano e respeitar os stops" />
        </div>
        <div className="mt-3">
          <Textarea
            label="Como estou me sentindo antes de operar?"
            value={pre.sentimentoAntes}
            onChange={(e) => setPre({ sentimentoAntes: e.target.value })}
            placeholder="Descreva seu estado mental e emocional agora."
          />
        </div>
      </Card>

      <Card>
        <CardHeader title="Checklist mental" subtitle="Marque apenas o que for verdade agora." />
        <div className="grid grid-cols-1 gap-2">
          {checks.map(([k, label]) => (
            <Checkbox key={k} checked={pre.checklist[k]} onChange={(v) => setCheck(k, v)} label={label} />
          ))}
        </div>
      </Card>
    </div>
  );
}

// ── Etapa 2 — Operações (com Freio de Emergência) ──────────────
function StepTrades({
  session,
  update,
}: {
  session: Session;
  update: (p: Partial<Session>) => void;
}) {
  const [brakeOpen, setBrakeOpen] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [pendingOverride, setPendingOverride] = useState(false);

  const onBrakeProceed = (event: BrakeEvent) => {
    // registra a decisão no "banco de dados" (sessão)
    update({ brakeEvents: [...session.brakeEvents, event] });
    setBrakeOpen(false);
    if (event.decisao === "voltou") return; // desistiu de operar
    setPendingOverride(event.riscoAlto);
    setFormOpen(true);
  };

  const addTrade = (t: Trade) => {
    update({ trades: [...session.trades, t] });
    setFormOpen(false);
    setPendingOverride(false);
  };

  const removeTrade = (id: string) =>
    update({ trades: session.trades.filter((t) => t.id !== id) });

  const net = sessionNet(session);

  return (
    <Card>
      <CardHeader
        title="Operações do dia"
        subtitle="Toda nova operação passa pelo Freio de Emergência."
        action={
          <Button onClick={() => setBrakeOpen(true)}>
            <Plus className="h-4 w-4" strokeWidth={2.5} /> Adicionar operação
          </Button>
        }
      />

      {session.trades.length === 0 ? (
        <div className="rounded-xl border border-dashed border-line2 bg-card2/40 py-12 text-center text-sm text-muted">
          Nenhuma operação registrada ainda.
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[640px] text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs text-muted">
                  <th className="pb-2 pr-3 font-medium">Ativo</th>
                  <th className="pb-2 pr-3 font-medium">Dir.</th>
                  <th className="pb-2 pr-3 font-medium">Hora</th>
                  <th className="pb-2 pr-3 font-medium">Setup</th>
                  <th className="pb-2 pr-3 font-medium">Lote</th>
                  <th className="pb-2 pr-3 text-right font-medium">Resultado</th>
                  <th className="pb-2 font-medium"></th>
                </tr>
              </thead>
              <tbody>
                {session.trades.map((t) => (
                  <tr key={t.id} className="border-b border-line/60">
                    <td className="py-2.5 pr-3 font-medium">{t.ativo}</td>
                    <td className="py-2.5 pr-3">
                      <Badge tone={t.direcao === "compra" ? "pos" : "neg"}>{t.direcao}</Badge>
                    </td>
                    <td className="py-2.5 pr-3 text-muted">{t.horario}</td>
                    <td className="py-2.5 pr-3 text-muted">{t.setup || "—"}</td>
                    <td className="py-2.5 pr-3 tabular-nums">{t.lote}</td>
                    <td className={`py-2.5 pr-3 text-right font-semibold tabular-nums ${t.resultado >= 0 ? "text-pos" : "text-neg"}`}>
                      {BRL(t.resultado)}
                      {t.brakeOverride && (
                        <span className="ml-1.5 align-middle text-[10px] text-warn" title="Registrada após alerta do Freio de Emergência">⚠</span>
                      )}
                    </td>
                    <td className="py-2.5 text-right">
                      <button onClick={() => removeTrade(t.id)} className="rounded-lg p-1.5 text-muted transition hover:bg-white/5 hover:text-neg">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 flex items-center justify-between rounded-xl bg-card2 px-4 py-3">
            <span className="text-sm text-muted">{session.trades.length} operações</span>
            <span className={`text-sm font-semibold ${net >= 0 ? "text-pos" : "text-neg"}`}>
              Resultado líquido: {BRL(net)}
            </span>
          </div>
        </>
      )}

      <EmergencyBrake open={brakeOpen} onClose={() => setBrakeOpen(false)} onProceed={onBrakeProceed} />
      <TradeForm open={formOpen} onClose={() => setFormOpen(false)} onSave={addTrade} brakeOverride={pendingOverride} />
    </Card>
  );
}

// ── Etapa 3 — Psicologia ───────────────────────────────────────
function StepPsych({
  session,
  update,
}: {
  session: Session;
  update: (p: Partial<Session>) => void;
}) {
  const p = session.psychology;
  const setP = (patch: Partial<typeof p>) => update({ psychology: { ...p, ...patch } });

  const questions: [keyof typeof p, string][] = [
    ["medo", "Senti medo?"],
    ["ansiedade", "Senti ansiedade?"],
    ["ganancia", "Senti ganância?"],
    ["fomo", "Senti FOMO?"],
    ["quisRecuperar", "Quis recuperar prejuízo?"],
    ["aumentouLote", "Aumentei o lote?"],
    ["desobedeceuRegra", "Desobedeci alguma regra?"],
  ];

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader title="O que passou pela sua mente" />
        <div className="space-y-3">
          <Textarea
            label="O que pensei durante as operações?"
            value={p.pensamentos}
            onChange={(e) => setP({ pensamentos: e.target.value })}
          />
          <Textarea
            label="O que senti?"
            value={p.sentimentos}
            onChange={(e) => setP({ sentimentos: e.target.value })}
          />
        </div>
      </Card>

      <Card>
        <CardHeader title="Gatilhos emocionais" subtitle="Responda com sinceridade — ninguém está julgando." />
        <div className="space-y-2.5">
          {questions.map(([k, label]) => (
            <div key={k} className="flex items-center justify-between rounded-xl bg-card2 px-3.5 py-2.5">
              <span className="text-sm">{label}</span>
              <Toggle checked={p[k] as boolean | null} onChange={(v) => setP({ [k]: v } as any)} />
            </div>
          ))}
          {p.desobedeceuRegra && (
            <div className="animate-fade-up pt-1">
              <Input
                label="Qual regra?"
                value={p.qualRegra}
                onChange={(e) => setP({ qualRegra: e.target.value })}
                placeholder="Descreva a regra que quebrou"
              />
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

// ── Etapa 4 — Autoavaliação (Radar) ────────────────────────────
function StepEval({
  session,
  update,
}: {
  session: Session;
  update: (p: Partial<Session>) => void;
}) {
  const e = session.selfEval;
  const setE = (patch: Partial<typeof e>) => update({ selfEval: { ...e, ...patch } });

  const radar = [
    { axis: "Disciplina", value: e.disciplina },
    { axis: "Execução", value: e.execucao },
    { axis: "Gestão de Risco", value: e.gestaoRisco },
    { axis: "Paciência", value: e.paciencia },
    { axis: "Controle Emocional", value: e.controleEmocional },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader title="Notas do dia" subtitle="De 0 a 100, avalie sua performance de processo." />
        <div className="space-y-5 pt-1">
          <Slider label="Disciplina" value={e.disciplina} onChange={(v) => setE({ disciplina: v })} color="#6C3EFF" />
          <Slider label="Execução" value={e.execucao} onChange={(v) => setE({ execucao: v })} color="#8A63FF" />
          <Slider label="Gestão de Risco" value={e.gestaoRisco} onChange={(v) => setE({ gestaoRisco: v })} color="#22C55E" />
          <Slider label="Paciência" value={e.paciencia} onChange={(v) => setE({ paciencia: v })} color="#F5B301" />
          <Slider label="Controle Emocional" value={e.controleEmocional} onChange={(v) => setE({ controleEmocional: v })} color="#EF4444" />
        </div>
      </Card>
      <Card>
        <CardHeader
          title="Radar de performance"
          subtitle={`Média geral: ${Math.round(evalAverage(e))}/100`}
        />
        <EmotionRadar data={radar} />
      </Card>
    </div>
  );
}

// ── Etapa 5 — Reflexão ─────────────────────────────────────────
function StepReflection({
  session,
  update,
}: {
  session: Session;
  update: (p: Partial<Session>) => void;
}) {
  const r = session.reflection;
  const setR = (patch: Partial<typeof r>) => update({ reflection: { ...r, ...patch } });

  return (
    <Card>
      <CardHeader title="Reflexão do dia" subtitle="O aprendizado vale mais que o resultado." />
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        <Textarea label="Maior erro do dia" value={r.maiorErro} onChange={(e) => setR({ maiorErro: e.target.value })} />
        <Textarea label="Maior acerto do dia" value={r.maiorAcerto} onChange={(e) => setR({ maiorAcerto: e.target.value })} />
        <Textarea label="Maior aprendizado" value={r.maiorAprendizado} onChange={(e) => setR({ maiorAprendizado: e.target.value })} />
        <Textarea label="O que nunca mais quero repetir?" value={r.nuncaRepetir} onChange={(e) => setR({ nuncaRepetir: e.target.value })} />
        <div className="md:col-span-2">
          <Textarea label="Compromisso para amanhã" value={r.compromissoAmanha} onChange={(e) => setR({ compromissoAmanha: e.target.value })} />
        </div>
      </div>
    </Card>
  );
}
