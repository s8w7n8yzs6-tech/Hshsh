"use client";

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  useCallback,
} from "react";
import type { Session, DeskConfig } from "./types";
import { defaultDesk } from "./defaults";
import { generateSeed } from "./seed";
import { useAuth } from "./auth";

interface StoreValue {
  ready: boolean;
  sessions: Session[];
  desk: DeskConfig;
  saveSession: (s: Session) => void;
  deleteSession: (id: string) => void;
  getSession: (id: string) => Session | undefined;
  getSessionByDate: (date: string) => Session | undefined;
  updateDesk: (d: Partial<DeskConfig>) => void;
  resetDemo: () => void;
}

const StoreContext = createContext<StoreValue | null>(null);

const keyFor = (uid: string) => `tm.data.${uid}`;

interface Persisted {
  sessions: Session[];
  desk: DeskConfig;
  seeded: boolean;
}

export function StoreProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [ready, setReady] = useState(false);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [desk, setDesk] = useState<DeskConfig>(defaultDesk);

  const storageKey = user ? keyFor(user.id) : null;

  // Load
  useEffect(() => {
    if (!storageKey) return;
    setReady(false);
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) {
        const data: Persisted = JSON.parse(raw);
        setSessions(data.sessions ?? []);
        setDesk({ ...defaultDesk, ...(data.desk ?? {}) });
      } else {
        // First login: seed with a realistic demo history
        const seeded = generateSeed();
        setSessions(seeded);
        setDesk(defaultDesk);
        localStorage.setItem(
          storageKey,
          JSON.stringify({ sessions: seeded, desk: defaultDesk, seeded: true })
        );
      }
    } catch {
      setSessions([]);
      setDesk(defaultDesk);
    }
    setReady(true);
  }, [storageKey]);

  const persist = useCallback(
    (next: Session[], nextDesk: DeskConfig) => {
      if (!storageKey) return;
      localStorage.setItem(
        storageKey,
        JSON.stringify({ sessions: next, desk: nextDesk, seeded: true })
      );
    },
    [storageKey]
  );

  const saveSession = useCallback(
    (s: Session) => {
      setSessions((prev) => {
        const idx = prev.findIndex((x) => x.id === s.id);
        const updated = { ...s, updatedAt: new Date().toISOString() };
        const next =
          idx >= 0
            ? prev.map((x) => (x.id === s.id ? updated : x))
            : [...prev, updated];
        persist(next, desk);
        return next;
      });
    },
    [persist, desk]
  );

  const deleteSession = useCallback(
    (id: string) => {
      setSessions((prev) => {
        const next = prev.filter((x) => x.id !== id);
        persist(next, desk);
        return next;
      });
    },
    [persist, desk]
  );

  const updateDesk = useCallback(
    (d: Partial<DeskConfig>) => {
      setDesk((prev) => {
        const next = { ...prev, ...d };
        persist(sessions, next);
        return next;
      });
    },
    [persist, sessions]
  );

  const resetDemo = useCallback(() => {
    const seeded = generateSeed();
    setSessions(seeded);
    setDesk(defaultDesk);
    persist(seeded, defaultDesk);
  }, [persist]);

  const getSession = useCallback((id: string) => sessions.find((s) => s.id === id), [sessions]);
  const getSessionByDate = useCallback(
    (date: string) => sessions.find((s) => s.pre.data === date),
    [sessions]
  );

  const value = useMemo(
    () => ({
      ready,
      sessions,
      desk,
      saveSession,
      deleteSession,
      getSession,
      getSessionByDate,
      updateDesk,
      resetDemo,
    }),
    [ready, sessions, desk, saveSession, deleteSession, getSession, getSessionByDate, updateDesk, resetDemo]
  );

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}

export function useStore() {
  const ctx = useContext(StoreContext);
  if (!ctx) throw new Error("useStore must be used within StoreProvider");
  return ctx;
}
