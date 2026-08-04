import type {
  DeskConfig,
  PreMarket,
  Psychology,
  SelfEval,
  Reflection,
  Session,
} from "./types";
import { uid } from "./id";

export const defaultDesk: DeskConfig = {
  metaMesa: 6000,
  drawdownMaximo: 4000,
  metaLucroDia: 500,
  duracaoDesafio: 30,
  saldoInicialMesa: 50000,
  inicioDesafio: new Date().toISOString().slice(0, 10),
};

export const emptyPre = (): PreMarket => ({
  data: new Date().toISOString().slice(0, 10),
  ativo: "WIN",
  conta: "",
  saldoInicial: 50000,
  objetivoDia: "",
  horario: "09:00",
  mesa: "",
  checklist: {
    dormiuBem: false,
    descansado: false,
    seguindoPlano: false,
    aceitaStop: false,
    naoPrecisaRecuperar: false,
    tranquilo: false,
    naoAnsioso: false,
    naoPorNecessidade: false,
  },
  sentimentoAntes: "",
});

export const emptyPsych = (): Psychology => ({
  pensamentos: "",
  sentimentos: "",
  medo: null,
  ansiedade: null,
  ganancia: null,
  fomo: null,
  quisRecuperar: null,
  aumentouLote: null,
  desobedeceuRegra: null,
  qualRegra: "",
});

export const emptyEval = (): SelfEval => ({
  disciplina: 70,
  execucao: 70,
  gestaoRisco: 70,
  paciencia: 70,
  controleEmocional: 70,
});

export const emptyReflection = (): Reflection => ({
  maiorErro: "",
  maiorAcerto: "",
  maiorAprendizado: "",
  nuncaRepetir: "",
  compromissoAmanha: "",
});

export const newSession = (): Session => ({
  id: uid(),
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  pre: emptyPre(),
  trades: [],
  psychology: emptyPsych(),
  selfEval: emptyEval(),
  reflection: emptyReflection(),
  brakeEvents: [],
  analysis: null,
});
