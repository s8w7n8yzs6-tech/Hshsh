"use client";

import { useState } from "react";
import type { Trade } from "@/lib/types";
import { uid } from "@/lib/id";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Input, Textarea, Select } from "@/components/ui/Input";
import { ImagePlus, X } from "lucide-react";

export function TradeForm({
  open,
  onClose,
  onSave,
  brakeOverride,
}: {
  open: boolean;
  onClose: () => void;
  onSave: (t: Trade) => void;
  brakeOverride?: boolean;
}) {
  const [t, setT] = useState<Trade>(blank());
  const [preview, setPreview] = useState<string | null>(null);

  function blank(): Trade {
    return {
      id: uid(),
      ativo: "WIN",
      direcao: "compra",
      horario: new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
      setup: "",
      lote: 1,
      stop: null,
      take: null,
      resultado: 0,
      screenshot: null,
      observacoes: "",
    };
  }

  const set = (patch: Partial<Trade>) => setT((prev) => ({ ...prev, ...patch }));

  const onFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      const url = reader.result as string;
      setPreview(url);
      set({ screenshot: url });
    };
    reader.readAsDataURL(f);
  };

  const save = () => {
    onSave({ ...t, brakeOverride });
    setT(blank());
    setPreview(null);
  };

  return (
    <Modal open={open} onClose={onClose} className="max-w-xl">
      <h3 className="mb-5 text-base font-semibold">Adicionar operação</h3>

      <div className="grid grid-cols-2 gap-3">
        <Input label="Ativo" value={t.ativo} onChange={(e) => set({ ativo: e.target.value })} placeholder="WIN, WDO, XAUUSD…" />
        <Select label="Compra / Venda" value={t.direcao} onChange={(e) => set({ direcao: e.target.value as any })}>
          <option value="compra">Compra</option>
          <option value="venda">Venda</option>
        </Select>
        <Input label="Horário" value={t.horario} onChange={(e) => set({ horario: e.target.value })} placeholder="HH:MM" />
        <Input label="Setup" value={t.setup} onChange={(e) => set({ setup: e.target.value })} placeholder="Pullback, Rompimento…" />
        <Input
          label="Lote"
          type="number"
          value={t.lote}
          onChange={(e) => set({ lote: Number(e.target.value) })}
          min={0}
        />
        <Input
          label="Resultado (R$)"
          type="number"
          value={t.resultado}
          onChange={(e) => set({ resultado: Number(e.target.value) })}
          placeholder="+ gain / - loss"
        />
        <Input
          label="Stop (pontos)"
          type="number"
          value={t.stop ?? ""}
          onChange={(e) => set({ stop: e.target.value === "" ? null : Number(e.target.value) })}
        />
        <Input
          label="Take (pontos)"
          type="number"
          value={t.take ?? ""}
          onChange={(e) => set({ take: e.target.value === "" ? null : Number(e.target.value) })}
        />
      </div>

      <div className="mt-3">
        <Textarea label="Observações" value={t.observacoes} onChange={(e) => set({ observacoes: e.target.value })} placeholder="Contexto, motivo da entrada, o que observou…" />
      </div>

      <div className="mt-3">
        <span className="label">Screenshot</span>
        {preview ? (
          <div className="relative inline-block">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={preview} alt="screenshot" className="max-h-40 rounded-xl border border-line2" />
            <button
              onClick={() => {
                setPreview(null);
                set({ screenshot: null });
              }}
              className="absolute -right-2 -top-2 rounded-full bg-neg p-1 text-white"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        ) : (
          <label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-dashed border-line2 bg-card2 px-4 py-6 text-sm text-muted transition hover:border-brand/40 hover:text-ink">
            <ImagePlus className="h-4 w-4" />
            Anexar imagem do gráfico
            <input type="file" accept="image/*" className="hidden" onChange={onFile} />
          </label>
        )}
      </div>

      <div className="mt-6 flex gap-3">
        <Button variant="ghost" onClick={onClose} className="flex-1">
          Cancelar
        </Button>
        <Button onClick={save} className="flex-1">
          Registrar operação
        </Button>
      </div>
    </Modal>
  );
}
