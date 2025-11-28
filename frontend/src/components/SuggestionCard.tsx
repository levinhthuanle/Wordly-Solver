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
}

const BASE_CLASS = "rounded-2xl px-5 py-4 border shadow-inner";

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
}: SuggestionCardProps) {
  return (
    <article className={`${BASE_CLASS} ${TONE_CLASS[tone]}`}>
      <header className="flex items-center justify-between">
        <div className="flex flex-col gap-1">
          {headline && (
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
              {headline}
            </p>
          )}
          <span className="text-3xl font-semibold tracking-[0.35em] text-neutral-900">
            {word}
          </span>
        </div>
        {badge && (
          <span className="text-[0.65rem] font-medium uppercase tracking-[0.25em] text-primary-600">
            {badge}
          </span>
        )}
      </header>

      {detail && <p className="mt-3 text-sm text-neutral-600">{detail}</p>}

      {footer && <div className="mt-4 text-xs text-neutral-400">{footer}</div>}
    </article>
  );
}
