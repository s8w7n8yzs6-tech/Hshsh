"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Logo } from "@/components/ui/Logo";
import { cn } from "@/lib/cn";
import {
  LayoutDashboard,
  BarChart3,
  Brain,
  CalendarDays,
  Trophy,
  FileText,
  Plus,
  LogOut,
  Menu,
  X,
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/statistics", label: "Estatísticas", icon: BarChart3 },
  { href: "/psychology", label: "Psicológico", icon: Brain },
  { href: "/challenge", label: "Desafio 30 Dias", icon: CalendarDays },
  { href: "/achievements", label: "Conquistas", icon: Trophy },
  { href: "/report", label: "Relatório", icon: FileText },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, signOut } = useAuth();
  const [open, setOpen] = useState(false);

  const NavLinks = ({ onClick }: { onClick?: () => void }) => (
    <nav className="flex flex-col gap-1">
      {NAV.map(({ href, label, icon: Icon }) => {
        const active = pathname === href || pathname.startsWith(href + "/");
        return (
          <Link
            key={href}
            href={href}
            onClick={onClick}
            className={cn(
              "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
              active
                ? "bg-brand-dim text-ink"
                : "text-muted hover:bg-white/5 hover:text-ink"
            )}
          >
            <Icon
              className={cn("h-4.5 w-4.5", active ? "text-brand-soft" : "text-muted group-hover:text-ink")}
              size={18}
            />
            {label}
          </Link>
        );
      })}
    </nav>
  );

  const SidebarBody = ({ onNav }: { onNav?: () => void }) => (
    <div className="flex h-full flex-col">
      <div className="px-2 pb-6 pt-1">
        <Logo />
      </div>

      <Link
        href="/session"
        onClick={onNav}
        className="btn-primary mb-6 w-full"
      >
        <Plus className="h-4 w-4" strokeWidth={2.5} />
        Nova Sessão
      </Link>

      <NavLinks onClick={onNav} />

      <div className="mt-auto">
        <div className="mb-3 rounded-xl border border-line bg-card2/50 p-3">
          <p className="text-[11px] font-medium text-brand-soft">Lembrete</p>
          <p className="mt-1 text-[11px] leading-relaxed text-muted">
            Processo acima do resultado. Disciplina hoje, liberdade amanhã.
          </p>
        </div>
        <div className="flex items-center gap-3 rounded-xl px-2 py-2">
          <div className="flex h-8 w-8 flex-none items-center justify-center rounded-full bg-brand/20 text-xs font-semibold text-brand-soft">
            {(user?.name ?? "T").slice(0, 1).toUpperCase()}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-ink">{user?.name}</p>
            <p className="truncate text-[11px] text-muted">{user?.email}</p>
          </div>
          <button
            onClick={async () => {
              await signOut();
              router.replace("/login");
            }}
            className="rounded-lg p-1.5 text-muted transition hover:bg-white/5 hover:text-neg"
            title="Sair"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen">
      {/* Desktop sidebar */}
      <aside className="fixed left-0 top-0 hidden h-screen w-[248px] flex-col border-r border-line bg-[#0F0F0F] p-4 lg:flex">
        <SidebarBody />
      </aside>

      {/* Mobile top bar */}
      <div className="fixed inset-x-0 top-0 z-30 flex items-center justify-between border-b border-line bg-bg/80 px-4 py-3 backdrop-blur lg:hidden">
        <Logo />
        <button onClick={() => setOpen(true)} className="btn-subtle p-2">
          <Menu className="h-5 w-5" />
        </button>
      </div>

      {/* Mobile drawer */}
      {open && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={() => setOpen(false)} />
          <div className="absolute left-0 top-0 h-full w-[280px] animate-scale-in border-r border-line bg-[#0F0F0F] p-4">
            <button
              onClick={() => setOpen(false)}
              className="absolute right-4 top-4 rounded-lg p-1.5 text-muted hover:bg-white/5"
            >
              <X className="h-5 w-5" />
            </button>
            <SidebarBody onNav={() => setOpen(false)} />
          </div>
        </div>
      )}

      {/* Content */}
      <main className="flex-1 lg:pl-[248px]">
        <div className="mx-auto max-w-6xl px-4 pb-16 pt-20 sm:px-6 lg:pt-8">{children}</div>
      </main>
    </div>
  );
}
