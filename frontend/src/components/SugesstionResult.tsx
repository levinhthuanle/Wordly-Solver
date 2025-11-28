"use client";

import { SuggestionCard } from "@/components/SuggestionCard";
import type { AISuggestion } from "@/utils/api-utils";

type SugesstionResultProps = {
  suggestion: AISuggestion | null;
  isLoading: boolean;
  className?: string;
};

const Placeholder = ({ className }: { className?: string }) => (
  <div
    className={
      className
        ? `${className} rounded-2xl border border-dashed border-neutral-200 bg-neutral-50/80 px-5 py-4 text-sm text-neutral-500`
        : "rounded-2xl border border-dashed border-neutral-200 bg-neutral-50/80 px-5 py-4 text-sm text-neutral-500"
    }
  >
    Request a suggestion once you have at least one guess.
  </div>
);

const LoadingSkeleton = ({ className }: { className?: string }) => (
  <div
    className={
      className
        ? `${className} animate-pulse rounded-2xl border border-neutral-100 bg-white/60 px-5 py-4`
        : "animate-pulse rounded-2xl border border-neutral-100 bg-white/60 px-5 py-4"
    }
  >
    <div className="h-4 w-24 rounded bg-neutral-200" />
    <div className="mt-4 h-8 w-full rounded bg-neutral-200" />
    <div className="mt-3 h-4 w-3/4 rounded bg-neutral-200" />
  </div>
);

export function SugesstionResult({ suggestion, isLoading, className }: SugesstionResultProps) {
  if (isLoading && !suggestion) {
    return <LoadingSkeleton className={className} />;
  }

  if (!suggestion) {
    return <Placeholder className={className} />;
  }

  const containerClass = className ? `${className} space-y-3` : "space-y-3";
  const alternateWords = suggestion.alternatives.slice(0, 4);

  return (
    <div className={containerClass}>
      <SuggestionCard
        tone="primary"
        word={suggestion.word}
        headline="Top recommendation"
        badge={`${Math.round(suggestion.confidence * 100)}% match`}
        detail={suggestion.reasoning}
        footer={`${suggestion.remaining_count} word${suggestion.remaining_count !== 1 ? "s" : ""} still in play`}
      />

      {alternateWords.length > 0 && (
        <div className="grid gap-3">
          {alternateWords.map((word, index) => (
            <SuggestionCard
              key={word}
              word={word}
              headline={`Alternative ${index + 2}`}
              badge="Agent pick"
              tone="neutral"
              detail="Great follow-up if the top choice misses."
            />
          ))}
        </div>
      )}
    </div>
  );
}
