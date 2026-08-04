"use client";

import { useEffect, useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Slider, Toggle } from "@/components/ui/Field";
import { Badge } from "@/components/ui/Badge";
import type { BrakeEvent } from "@/lib/types";
import { uid } from "@/lib/id";
import { ShieldAlert, AlertTriangle, ArrowLeft, Timer } from "lucide-react";

// Avalia o risco emocional a partir das respostas.
export function assessRisk(a: {
  stopsHoje: number;
  saldoStatus: "positivo" | "negativo";
  motivo: "setup" | "recuperar";
  emocional: number;
  dormiuBem: boolean;
  cansado: boolean;
  ansioso: boolean;
}): boolean {
  let score = 0;
  if (a.motivo === "recuperar") score += 3; // gatilho mais perigoso
  if (a.stopsHoje >= 3) score += 2;
  else if (a.stopsHoje === 2) score += 1;
  if (a.saldoStatus === "negativo") score += 1;
  if (a.emocional <= 4) score += 2;
  if (!a.dormiuBem) score += 1;
  if (a.cansado) score += 1;
  if (a.ansioso) score += 1;
  return score >= 4;
}

export function EmergencyBrake({
  open,
  onClose,
  onProceed,
}: {
  open: boolean;
  onClose: () => void;
  onProceed: (event: BrakeEvent) => void;
}) {
  const [stopsHoje, setStops] = useState(0);
  const [saldoStatus, setSaldo] = useState<"positivo" | "negativo">("positivo");
  const [motivo, setMotivo] = useState<"setup" | "recuperar">("setup");
  const [emocional, setEmocional] = useState(7);
  const [dormiuBem, setDormiu] = useState<boolean | null>(true);
  const [cansado, setCansado] = useState<boolean | null>(false);
  const [ansioso, setAnsioso] = useState<boolean | null>(false);

  const [phase, setPhase] = useState<"quiz" | "warning">("quiz");
  const [countdown, setCountdown] = useState(30);

  useEffect(() => {
    if (!open) {
      setPhase("quiz");
      setCountdown(30);
    }
  }, [open]);

  useEffect(() => {
    if (phase !== "warning") return;
    setCountdown(30);
    const t = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) {
          clearInterval(t);
          return 0;
        }
        return c - 1;
      });
    }, 1000);
    return () => clearInterval(t);
  }, [phase]);

  const buildEvent = (decisao: "continuou" | "voltou" | null, risco: boolean): BrakeEvent => ({
    id: uid(),
    timestamp: new Date().toISOString(),
    stopsHoje,
    saldoStatus,
    motivo,
    emocional,
    dormiuBem: !!dormiuBem,
    cansado: !!cansado,
    ansioso: !!ansioso,
    riscoAlto: risco,
    decisao,
  });

  const evaluate = () => {
    const risco = assessRisk({ stopsHoje, saldoStatus, motivo, emocional, dormiuBem: !!dormiuBem, cansado: !!cansado, ansioso: !!ansioso });
    if (risco) {
      setPhase("warning");
    } else {
      onProceed(buildEvent("continuou", false));
    }
  };

  return (
    <Modal open={open} onClose={onClose} dismissable={phase === "quiz"} className="max-w-md">
      {phase === "quiz" ? (
        <div>
          <div className="mb-5 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-dim">
              <ShieldAlert className="h-5 w-5 text-brand-soft" />
            </div>
            <div>
              <h3 className="text-base font-semibold">Freio de Emergência</h3>
              <p className="text-xs text-muted">Responda com honestidade antes de operar.</p>
            </div>
          </div>

          <div className="space-y-5">
            <Slider label="Quantos stops tomou hoje?" value={stopsHoje} onChange={setStops} min={0} max={10} color="#EF4444" />

            <div>
              <span className="label">Está positivo ou negativo?</span>
              <div className="inline-flex w-full rounded-xl border border-line2 bg-card2 p-1">
                <button
                  onClick={() => setSaldo("positivo")}
                  className={`flex-1 rounded-lg py-2 text-sm font-medium transition ${saldoStatus === "positivo" ? "bg-pos/20 text-pos" : "text-muted"}`}
                >
                  Positivo
                </button>
                <button
                  onClick={() => setSaldo("negativo")}
                  className={`flex-1 rounded-lg py-2 text-sm font-medium transition ${saldoStatus === "negativo" ? "bg-neg/20 text-neg" : "text-muted"}`}
                >
                  Negativo
                </button>
              </div>
            </div>

            <div>
              <span className="label">Está operando porque…</span>
              <div className="grid grid-cols-1 gap-2">
                <button
                  onClick={() => setMotivo("setup")}
                  className={`rounded-xl border px-3.5 py-2.5 text-left text-sm transition ${motivo === "setup" ? "border-pos/40 bg-pos/10 text-ink" : "border-line2 bg-card2 text-muted"}`}
                >
                  Apareceu um setup válido
                </button>
                <button
                  onClick={() => setMotivo("recuperar")}
                  className={`rounded-xl border px-3.5 py-2.5 text-left text-sm transition ${motivo === "recuperar" ? "border-neg/40 bg-neg/10 text-ink" : "border-line2 bg-card2 text-muted"}`}
                >
                  Quero recuperar o que perdi
                </button>
              </div>
            </div>

            <Slider
              label="De 0 a 10, como está seu emocional?"
              value={emocional}
              onChange={setEmocional}
              min={0}
              max={10}
              color={emocional <= 4 ? "#EF4444" : emocional <= 6 ? "#F5B301" : "#22C55E"}
            />

            <div className="grid grid-cols-1 gap-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Dormiu bem?</span>
                <Toggle checked={dormiuBem} onChange={setDormiu} />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Está cansado?</span>
                <Toggle checked={cansado} onChange={setCansado} />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Está ansioso?</span>
                <Toggle checked={ansioso} onChange={setAnsioso} />
              </div>
            </div>
          </div>

          <div className="mt-6 flex gap-3">
            <Button variant="ghost" onClick={onClose} className="flex-1">
              Cancelar
            </Button>
            <Button onClick={evaluate} className="flex-1">
              Avaliar
            </Button>
          </div>
        </div>
      ) : (
        <WarningScreen
          countdown={countdown}
          onBack={() => {
            onProceed(buildEvent("voltou", true));
          }}
          onProceed={() => {
            onProceed(buildEvent("continuou", true));
          }}
        />
      )}
    </Modal>
  );
}

function WarningScreen({
  countdown,
  onBack,
  onProceed,
}: {
  countdown: number;
  onBack: () => void;
  onProceed: () => void;
}) {
  const locked = countdown > 0;
  return (
    <div className="text-center">
      <div className="mx-auto mb-5 flex h-16 w-16 animate-pulse-ring items-center justify-center rounded-2xl bg-neg/15">
        <AlertTriangle className="h-8 w-8 text-neg" />
      </div>
      <Badge tone="neg" className="mb-4">
        Risco emocional elevado
      </Badge>
      <h3 className="text-lg font-semibold leading-snug">Reflita antes de continuar</h3>
      <p className="mx-auto mt-3 max-w-sm text-sm leading-relaxed text-muted">
        Seu histórico mostra que, neste estado emocional, você costuma quebrar seu gerenciamento.
        Respire. O próximo trade não precisa acontecer agora.
      </p>

      {locked && (
        <div className="mt-6 flex items-center justify-center gap-2 text-sm text-muted">
          <Timer className="h-4 w-4" />
          Aguarde <span className="font-semibold tabular-nums text-ink">{countdown}s</span> para poder registrar.
        </div>
      )}

      <div className="mt-6 flex flex-col gap-3">
        <Button onClick={onBack} variant="primary" className="w-full">
          <ArrowLeft className="h-4 w-4" /> Voltar (recomendado)
        </Button>
        <Button onClick={onProceed} variant="danger" disabled={locked} className="w-full">
          {locked ? `Continuar mesmo assim (${countdown}s)` : "Continuar mesmo assim"}
        </Button>
      </div>
    </div>
  );
}
