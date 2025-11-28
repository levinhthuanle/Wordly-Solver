"use client";

import type { ReactNode } from "react";

export type SuggestionCardTone = "primary" | "neutral";

export interface SuggestionCardProps {
  word: string;
  headline?: string;
  badge?: string;
  detail?: string;
  tone?: SuggestionCardTone;
  footer?: ReactNode;
  onSelect?: () => void;
  disabled?: boolean;
}

const BASE_CLASS = "rounded-2xl px-5 py-5 border shadow-inner text-left";

const TONE_CLASS: Record<SuggestionCardTone, string> = {
  primary: "border-neutral-100 bg-gradient-to-br from-white to-neutral-50",
  neutral: "border-neutral-200 bg-white/90 shadow-soft",
};

export function SuggestionCard({
  word,
  headline,
  badge,
  detail,
  tone = "neutral",
  footer,
  onSelect,
  disabled = false,
}: SuggestionCardProps) {
  const isInteractive = Boolean(onSelect);
  const canClick = isInteractive && !disabled;

  const interactiveClass = isInteractive
    ? `transition ${canClick ? "cursor-pointer hover:-translate-y-0.5 hover:shadow-lg" : "cursor-not-allowed opacity-60"} focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neutral-400`
    : "";

  const className = `${BASE_CLASS} ${TONE_CLASS[tone]} ${interactiveClass}`.trim();
  const Container = isInteractive ? "button" : "article";

 

  return (
    <Container
      type={isInteractive ? "button" : undefined}
      onClick={canClick ? onSelect : undefined}
      disabled={isInteractive ? disabled : undefined}
      aria-disabled={isInteractive ? disabled : undefined}
      className={className}
    >
      <header className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          {headline && (
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
              {headline}
            </p>
          )}
          <span className="text-4xl font-semibold tracking-[0.35em] text-neutral-900">
            {word}
          </span>
        </div>
        {badge && (
          <span className="text-[0.65rem] font-medium uppercase tracking-[0.25em] text-primary-600 whitespace-nowrap">
            {badge}
          </span>
        )}
      </header>

      {detail && <p className="mt-3 text-sm leading-relaxed text-neutral-600">{detail}</p>}

      {footer && <div className="mt-4 text-xs text-neutral-400">{footer}</div>}

    </Container>
  );
}

function ArrowIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M4 10h11m0 0-4-4m4 4-4 4"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
