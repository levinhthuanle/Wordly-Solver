"use client";

import type { AISuggestion } from "@/utils/api-utils";

type SugesstionResultProps = {
  suggestion: AISuggestion | null;
  isLoading: boolean;
  className?: string;
};

export function SugesstionResult({ suggestion, isLoading, className }: SugesstionResultProps) {
  const baseClass = "rounded-2xl px-5 py-4";

  if (!suggestion) {
    const placeholderClass = className
      ? `${baseClass} border border-dashed border-neutral-200 bg-neutral-50/80 text-sm text-neutral-500 ${className}`
      : `${baseClass} border border-dashed border-neutral-200 bg-neutral-50/80 text-sm text-neutral-500`;

    return (
      <div className={placeholderClass}>
        {isLoading
          ? "Crunching possibilities…"
          : "Request a suggestion once you have at least one guess."}
      </div>
    );
  }

  const suggestionClass = className
    ? `${baseClass} border border-primary-100 bg-gradient-to-br from-primary-50 to-white shadow-inner ${className}`
    : `${baseClass} border border-primary-100 bg-gradient-to-br from-primary-50 to-white shadow-inner`;

  return (
    <div className={suggestionClass}>
      <div className="flex items-center justify-between">
        <span className="text-3xl font-semibold tracking-[0.4em] text-neutral-900">
          {suggestion.word}
        </span>
        <span className="text-xs font-medium text-primary-600">
          {Math.round(suggestion.confidence * 100)}% match
        </span>
      </div>
      <p className="mt-3 text-sm text-neutral-600">{suggestion.reasoning}</p>
      <p className="mt-2 text-xs font-medium text-neutral-400">
        {suggestion.remaining_count} word
        {suggestion.remaining_count !== 1 ? "s" : ""} still in play
      </p>
    </div>
  );
}
