"use client";

import { cn } from "@/lib/cn";
import { Loader2 } from "lucide-react";

type Variant = "primary" | "ghost" | "subtle" | "danger";

export function Button({
  variant = "primary",
  loading,
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  loading?: boolean;
}) {
  const styles: Record<Variant, string> = {
    primary: "btn-primary",
    ghost: "btn-ghost",
    subtle: "btn-subtle",
    danger:
      "btn bg-neg/90 text-white hover:bg-neg shadow-[0_8px_30px_-10px_rgba(239,68,68,0.7)]",
  };
  return (
    <button
      className={cn(styles[variant], className)}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading && <Loader2 className="h-4 w-4 animate-spin" />}
      {children}
    </button>
  );
}
