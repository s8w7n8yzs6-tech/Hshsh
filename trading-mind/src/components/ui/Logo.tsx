import { cn } from "@/lib/cn";

export function Logo({
  className,
  showText = true,
}: {
  className?: string;
  showText?: boolean;
}) {
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      <div className="relative flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-brand to-brand-soft shadow-[0_6px_20px_-6px_rgba(108,62,255,0.8)]">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          className="h-4.5 w-4.5"
          width={18}
          height={18}
        >
          <path
            d="M4 15c2-1 3-6 5-6s2 5 4 5 3-8 5-8"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      {showText && (
        <span className="text-[15px] font-semibold tracking-tight text-ink">
          Trading Mind
        </span>
      )}
    </div>
  );
}
