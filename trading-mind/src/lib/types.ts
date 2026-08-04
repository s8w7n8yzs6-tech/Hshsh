// ─────────────────────────────────────────────────────────────
// Domain model — Trading Mind
// ─────────────────────────────────────────────────────────────

export type Direction = "compra" | "venda";
export type TradeResult = "gain" | "loss" | "breakeven";

export interface Trade {
  id: string;
  ativo: string;
  direcao: Direction;
  horario: string; // HH:MM
  setup: string;
  lote: number;
  stop: number | null; // pontos/preço de stop
  take: number | null; // pontos/preço de alvo
  resultado: number; // R$ (positivo gain, negativo loss)
  screenshot?: string | null; // data URL / storage path
  observacoes?: string;
  // decisão registrada pelo Freio de Emergência (se houve)
  brakeOverride?: boolean;
}

export interface PreMarket {
  data: string; // YYYY-MM-DD
  ativo: string;
  conta: string;
  saldoInicial: number;
  objetivoDia: string;
  horario: string;
  mesa: string;
  checklist: {
    dormiuBem: boolean;
    descansado: boolean;
    seguindoPlano: boolean;
    aceitaStop: boolean;
    naoPrecisaRecuperar: boolean;
    tranquilo: boolean;
    naoAnsioso: boolean;
    naoPorNecessidade: boolean;
  };
  sentimentoAntes: string;
}

export interface Psychology {
  pensamentos: string;
  sentimentos: string;
  medo: boolean | null;
  ansiedade: boolean | null;
  ganancia: boolean | null;
  fomo: boolean | null;
  quisRecuperar: boolean | null;
  aumentouLote: boolean | null;
  desobedeceuRegra: boolean | null;
  qualRegra: string;
}

export interface SelfEval {
  disciplina: number; // 0-100
  execucao: number;
  gestaoRisco: number;
  paciencia: number;
  controleEmocional: number;
}

export interface Reflection {
  maiorErro: string;
  maiorAcerto: string;
  maiorAprendizado: string;
  nuncaRepetir: string;
  compromissoAmanha: string;
}

// Registro do Freio de Emergência (por sessão pode haver vários)
export interface BrakeEvent {
  id: string;
  timestamp: string;
  stopsHoje: number;
  saldoStatus: "positivo" | "negativo";
  motivo: "setup" | "recuperar";
  emocional: number; // 0-10
  dormiuBem: boolean;
  cansado: boolean;
  ansioso: boolean;
  riscoAlto: boolean;
  decisao: "continuou" | "voltou" | null;
}

export interface AIAnalysis {
  resumo: string;
  pontosFortes: string[];
  pontosFracos: string[];
  planoMelhoria: string[];
  exercicioMental: string;
  fraseDoDia: string;
  padroes: string[]; // ex: "Revenge Trade", "Overtrade"
  geradoEm: string;
  fonte: "ia" | "local";
}

export interface Session {
  id: string;
  createdAt: string;
  updatedAt: string;
  pre: PreMarket;
  trades: Trade[];
  psychology: Psychology;
  selfEval: SelfEval;
  reflection: Reflection;
  brakeEvents: BrakeEvent[];
  analysis?: AIAnalysis | null;
}

export interface DeskConfig {
  metaMesa: number; // meta de lucro para aprovação (R$)
  drawdownMaximo: number; // limite de perda (R$)
  metaLucroDia: number; // meta diária (R$)
  duracaoDesafio: number; // dias (default 30)
  saldoInicialMesa: number;
  inicioDesafio: string; // YYYY-MM-DD
}

export type DayClassification =
  | "cinza" // sem operação
  | "verde" // disciplinado
  | "amarelo" // pequenos erros
  | "vermelho" // quebra de gerenciamento
  | "roxo"; // execução perfeita

export interface Profile {
  id: string;
  name: string;
  email: string;
  desk: DeskConfig;
}
