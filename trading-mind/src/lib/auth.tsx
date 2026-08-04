"use client";

import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { getSupabase, supabaseEnabled } from "./supabase";

interface AuthUser {
  id: string;
  email: string;
  name: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);
const LS_KEY = "tm.auth.user";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sb = getSupabase();
    if (sb) {
      sb.auth.getSession().then(({ data }) => {
        const u = data.session?.user;
        if (u)
          setUser({
            id: u.id,
            email: u.email ?? "",
            name: (u.user_metadata?.name as string) ?? u.email?.split("@")[0] ?? "Trader",
          });
        setLoading(false);
      });
      const { data: sub } = sb.auth.onAuthStateChange((_e, session) => {
        const u = session?.user;
        setUser(
          u
            ? {
                id: u.id,
                email: u.email ?? "",
                name: (u.user_metadata?.name as string) ?? u.email?.split("@")[0] ?? "Trader",
              }
            : null
        );
      });
      return () => sub.subscription.unsubscribe();
    }
    // demo mode
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (raw) setUser(JSON.parse(raw));
    } catch {}
    setLoading(false);
  }, []);

  const persistDemo = (u: AuthUser | null) => {
    setUser(u);
    if (u) localStorage.setItem(LS_KEY, JSON.stringify(u));
    else localStorage.removeItem(LS_KEY);
  };

  const signIn = useCallback(async (email: string, password: string) => {
    const sb = getSupabase();
    if (sb) {
      const { error } = await sb.auth.signInWithPassword({ email, password });
      if (error) throw error;
      return;
    }
    if (!email || !password) throw new Error("Informe email e senha.");
    persistDemo({ id: "demo-" + btoa(email).slice(0, 8), email, name: email.split("@")[0] });
  }, []);

  const signUp = useCallback(async (name: string, email: string, password: string) => {
    const sb = getSupabase();
    if (sb) {
      const { error } = await sb.auth.signUp({
        email,
        password,
        options: { data: { name } },
      });
      if (error) throw error;
      return;
    }
    if (!email || !password) throw new Error("Preencha os campos.");
    persistDemo({ id: "demo-" + btoa(email).slice(0, 8), email, name: name || email.split("@")[0] });
  }, []);

  const signInWithGoogle = useCallback(async () => {
    const sb = getSupabase();
    if (sb) {
      const { error } = await sb.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo: window.location.origin + "/dashboard" },
      });
      if (error) throw error;
      return;
    }
    persistDemo({ id: "demo-google", email: "trader@google.com", name: "Trader" });
  }, []);

  const resetPassword = useCallback(async (email: string) => {
    const sb = getSupabase();
    if (sb) {
      const { error } = await sb.auth.resetPasswordForEmail(email, {
        redirectTo: window.location.origin + "/login",
      });
      if (error) throw error;
    }
    // demo: no-op
  }, []);

  const signOut = useCallback(async () => {
    const sb = getSupabase();
    if (sb) await sb.auth.signOut();
    persistDemo(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, signIn, signUp, signInWithGoogle, resetPassword, signOut }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export { supabaseEnabled };
