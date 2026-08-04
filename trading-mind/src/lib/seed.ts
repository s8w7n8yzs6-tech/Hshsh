import type { Session, Trade } from "./types";
import { uid } from "./id";
import {
  emptyPre,
  emptyPsych,
  emptyEval,
  emptyReflection,
} from "./defaults";

const SETUPS = ["Pullback", "Rompimento", "Suporte/Resistência", "Fibo", "Reversão"];
const ATIVOS = ["WIN", "WDO", "XAUUSD", "NAS100"];
const HORAS = ["09:12", "09:45", "10:20", "10:58", "11:30", "14:05", "15:10"];

function mkTrade(win: boolean, lote: number, ativo: string): Trade {
  const base = ativo === "WIN" ? 150 : ativo === "WDO" ? 200 : 120;
  const mag = base * lote * (0.6 + Math.random());
  return {
    id: uid(),
    ativo,
    direcao: Math.random() > 0.5 ? "compra" : "venda",
    horario: HORAS[Math.floor(Math.random() * HORAS.length)],
    setup: SETUPS[Math.floor(Math.random() * SETUPS.length)],
    lote,
    stop: Math.round(base * 0.8),
    take: Math.round(base * 1.6),
    resultado: Math.round(win ? mag : -mag * 0.8),
    observacoes: "",
  };
}

// Gera um histórico realista com dias bons, medianos e um dia de revenge trade.
export function generateSeed(): Session[] {
  const days = 14;
  const today = new Date();
  const sessions: Session[] = [];

  for (let i = days; i >= 1; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    if (d.getDay() === 0 || d.getDay() === 6) continue; // sem fim de semana
    const dateStr = d.toISOString().slice(0, 10);

    const archetype = Math.random();
    const ativo = ATIVOS[Math.floor(Math.random() * 2)];
    const s: Session = {
      id: uid(),
      createdAt: d.toISOString(),
      updatedAt: d.toISOString(),
      pre: {
        ...emptyPre(),
        data: dateStr,
        ativo,
        conta: "Mesa Alpha",
        mesa: "Alpha 50k",
        objetivoDia: "Seguir o plano e respeitar os stops.",
        checklist: {
          dormiuBem: archetype > 0.3,
          descansado: archetype > 0.4,
          seguindoPlano: archetype > 0.25,
          aceitaStop: archetype > 0.3,
          naoPrecisaRecuperar: archetype > 0.35,
          tranquilo: archetype > 0.4,
          naoAnsioso: archetype > 0.45,
          naoPorNecessidade: true,
        },
        sentimentoAntes:
          archetype > 0.5 ? "Focado e tranquilo." : "Um pouco ansioso hoje.",
      },
      trades: [],
      psychology: emptyPsych(),
      selfEval: emptyEval(),
      reflection: {
        ...emptyReflection(),
        maiorAprendizado: "Paciência para esperar o setup.",
        compromissoAmanha: "Operar menos e melhor.",
      },
      brakeEvents: [],
      analysis: null,
    };

    if (archetype > 0.72) {
      // Dia perfeito
      s.trades = [mkTrade(true, 1, ativo), mkTrade(true, 1, ativo)];
      s.selfEval = { disciplina: 95, execucao: 92, gestaoRisco: 94, paciencia: 93, controleEmocional: 96 };
      s.psychology = { ...emptyPsych(), medo: false, ansiedade: false, ganancia: false, fomo: false, quisRecuperar: false, aumentouLote: false, desobedeceuRegra: false };
    } else if (archetype > 0.4) {
      // Dia bom/mediano
      const wins = Math.random() > 0.4;
      s.trades = [mkTrade(true, 1, ativo), mkTrade(wins, 1, ativo), mkTrade(true, 1, ativo)];
      s.selfEval = { disciplina: 78, execucao: 74, gestaoRisco: 80, paciencia: 72, controleEmocional: 76 };
      s.psychology = { ...emptyPsych(), medo: false, ansiedade: true, ganancia: false, fomo: false, quisRecuperar: false, aumentouLote: false, desobedeceuRegra: false };
    } else if (archetype > 0.18) {
      // Pequenos erros
      s.trades = [mkTrade(false, 1, ativo), mkTrade(true, 1, ativo), mkTrade(false, 2, ativo), mkTrade(true, 1, ativo)];
      s.selfEval = { disciplina: 62, execucao: 58, gestaoRisco: 55, paciencia: 50, controleEmocional: 60 };
      s.psychology = { ...emptyPsych(), medo: true, ansiedade: true, ganancia: false, fomo: true, quisRecuperar: false, aumentouLote: false, desobedeceuRegra: false };
    } else {
      // Revenge trade / quebra de gerenciamento
      s.trades = [
        mkTrade(false, 1, ativo),
        mkTrade(false, 2, ativo),
        mkTrade(false, 3, ativo),
        mkTrade(false, 4, ativo),
        mkTrade(true, 2, ativo),
      ];
      s.selfEval = { disciplina: 32, execucao: 40, gestaoRisco: 28, paciencia: 25, controleEmocional: 30 };
      s.psychology = {
        pensamentos: "Preciso recuperar o que perdi.",
        sentimentos: "Frustrado e revoltado.",
        medo: false,
        ansiedade: true,
        ganancia: true,
        fomo: false,
        quisRecuperar: true,
        aumentouLote: true,
        desobedeceuRegra: true,
        qualRegra: "Aumentei o lote após stops seguidos.",
      };
      s.brakeEvents = [
        {
          id: uid(),
          timestamp: d.toISOString(),
          stopsHoje: 3,
          saldoStatus: "negativo",
          motivo: "recuperar",
          emocional: 2,
          dormiuBem: false,
          cansado: true,
          ansioso: true,
          riscoAlto: true,
          decisao: "continuou",
        },
      ];
      s.reflection = {
        maiorErro: "Aumentei o lote para recuperar.",
        maiorAcerto: "Parei antes de zerar o dia.",
        maiorAprendizado: "Revenge trade destrói o gerenciamento.",
        nuncaRepetir: "Operar para recuperar prejuízo.",
        compromissoAmanha: "Respeitar o limite de 2 stops.",
      };
    }

    sessions.push(s);
  }

  return sessions;
}
