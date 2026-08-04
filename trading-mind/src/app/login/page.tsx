"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth, supabaseEnabled } from "@/lib/auth";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Mail, Lock, User, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";

type Mode = "login" | "signup" | "reset";

export default function LoginPage() {
  const { user, loading, signIn, signUp, signInWithGoogle, resetPassword } = useAuth();
  const router = useRouter();
  const [mode, setMode] = useState<Mode>("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");

  useEffect(() => {
    if (!loading && user) router.replace("/dashboard");
  }, [user, loading, router]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setInfo("");
    setBusy(true);
    try {
      if (mode === "login") {
        await signIn(email, password);
        router.replace("/dashboard");
      } else if (mode === "signup") {
        await signUp(name, email, password);
        if (supabaseEnabled) setInfo("Conta criada! Verifique seu email para confirmar.");
        else router.replace("/dashboard");
      } else {
        await resetPassword(email);
        setInfo("Se o email existir, enviamos um link de recuperação.");
      }
    } catch (err: any) {
      setError(err?.message ?? "Algo deu errado. Tente novamente.");
    } finally {
      setBusy(false);
    }
  };

  const google = async () => {
    setError("");
    setBusy(true);
    try {
      await signInWithGoogle();
      if (!supabaseEnabled) router.replace("/dashboard");
    } catch (err: any) {
      setError(err?.message ?? "Falha no login com Google.");
      setBusy(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-10">
      {/* ambient background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-brand/20 blur-[120px]" />
        <div className="absolute bottom-0 right-0 h-[380px] w-[380px] rounded-full bg-brand/10 blur-[120px]" />
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,.6) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.6) 1px, transparent 1px)",
            backgroundSize: "56px 56px",
          }}
        />
      </div>

      <div className="relative z-10 w-full max-w-[400px] animate-fade-up">
        <div className="mb-8 flex flex-col items-center text-center">
          <Logo showText={false} className="mb-4 scale-125" />
          <h1 className="text-2xl font-semibold tracking-tight">
            {mode === "login" ? "Bem-vindo de volta" : mode === "signup" ? "Crie sua conta" : "Recuperar senha"}
          </h1>
          <p className="mt-1.5 text-sm text-muted">
            {mode === "reset"
              ? "Enviaremos um link para redefinir sua senha."
              : "Processo acima do resultado."}
          </p>
        </div>

        <div className="card-base p-6">
          <form onSubmit={submit} className="space-y-3.5">
            {mode === "signup" && (
              <div className="relative">
                <User className="pointer-events-none absolute left-3 top-[38px] h-4 w-4 text-muted" />
                <Input
                  label="Nome"
                  id="name"
                  className="pl-9"
                  placeholder="Seu nome"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            )}

            <div className="relative">
              <Mail className="pointer-events-none absolute left-3 top-[38px] h-4 w-4 text-muted" />
              <Input
                label="Email"
                id="email"
                type="email"
                className="pl-9"
                placeholder="voce@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            {mode !== "reset" && (
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-[38px] h-4 w-4 text-muted" />
                <Input
                  label="Senha"
                  id="password"
                  type="password"
                  className="pl-9"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            )}

            {mode === "login" && (
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={() => setMode("reset")}
                  className="text-xs text-muted transition hover:text-ink"
                >
                  Esqueci minha senha
                </button>
              </div>
            )}

            {error && (
              <div className="flex items-start gap-2 rounded-xl border border-neg/25 bg-neg/10 px-3 py-2.5 text-xs text-neg">
                <AlertCircle className="mt-0.5 h-3.5 w-3.5 flex-none" />
                <span>{error}</span>
              </div>
            )}
            {info && (
              <div className="flex items-start gap-2 rounded-xl border border-pos/25 bg-pos/10 px-3 py-2.5 text-xs text-pos">
                <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 flex-none" />
                <span>{info}</span>
              </div>
            )}

            <Button type="submit" loading={busy} className="w-full">
              {mode === "login" ? "Entrar" : mode === "signup" ? "Criar conta" : "Enviar link"}
              {!busy && <ArrowRight className="h-4 w-4" />}
            </Button>
          </form>

          {mode !== "reset" && (
            <>
              <div className="my-4 flex items-center gap-3">
                <div className="h-px flex-1 bg-line" />
                <span className="text-xs text-muted">ou</span>
                <div className="h-px flex-1 bg-line" />
              </div>

              <button
                onClick={google}
                disabled={busy}
                className="btn-ghost w-full disabled:opacity-40"
              >
                <GoogleIcon />
                Continuar com Google
              </button>
            </>
          )}

          <p className="mt-5 text-center text-xs text-muted">
            {mode === "login" ? (
              <>
                Não tem conta?{" "}
                <button onClick={() => setMode("signup")} className="font-medium text-brand-soft hover:underline">
                  Cadastre-se
                </button>
              </>
            ) : (
              <>
                Já tem conta?{" "}
                <button onClick={() => setMode("login")} className="font-medium text-brand-soft hover:underline">
                  Entrar
                </button>
              </>
            )}
          </p>
        </div>

        {!supabaseEnabled && (
          <p className="mt-4 text-center text-[11px] leading-relaxed text-muted/70">
            Modo demonstração ativo — os dados ficam salvos no seu navegador.
            <br /> Configure o Supabase no <code className="text-muted">.env.local</code> para ativar o backend real.
          </p>
        )}
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1Z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23Z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84Z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38Z"
      />
    </svg>
  );
}
