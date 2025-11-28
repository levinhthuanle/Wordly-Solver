"use client";

import { BUTTON } from "@/constants/constants";
import type { SolverStrategy } from "@/types/types";
import type { Dispatch, SetStateAction } from "react";

type AISuggestionPanelProps = {
  selectedAlgorithm: SolverStrategy;
  setSelectedAlgorithm: Dispatch<SetStateAction<SolverStrategy>>;
  getSuggestion: () => void;
  clearSuggestion: () => void;
  isLoading: boolean;
  error: string | null;
  hasSuggestion: boolean;
};

const ALGORITHMS: { value: SolverStrategy; label: string }[] = [
  { value: "random", label: "Random" },
  { value: "frequency", label: "Frequency" },
  { value: "entropy", label: "Entropy" },
  { value: "better_entropy", label: "Better Entropy" },
];

export function AISuggestionPanel({
  selectedAlgorithm,
  setSelectedAlgorithm,
  getSuggestion,
  clearSuggestion,
  isLoading,
  error,
  hasSuggestion,
}: AISuggestionPanelProps) {
  const statusMessage = (() => {
    if (isLoading) {
      return "Analyzing your previous guesses";
    }
    if (hasSuggestion) {
      return "Tap Clear to explore a different strategy";
    }
    return "Select a strategy to begin";
  })();

  return (
    <div className="mt-8 w-full max-w-md">
      <section className="w-full rounded-2xl bg-white/85 p-6 shadow-soft ring-1 ring-neutral-200/70 backdrop-blur">
        <header className="flex flex-col gap-4">
          <div className="space-y-1">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary-500">
              AI Assistant
            </p>
            <h2 className="text-xl font-semibold text-neutral-900">
              Smarter guesses in one tap
            </h2>
            <p className="text-sm text-neutral-500">
              Let the solver scan your history and surface the next best move.
            </p>
          </div>

          <div className="rounded-2xl border border-neutral-200 bg-neutral-50/80 p-4 text-sm text-neutral-700">
            <div className="flex flex-wrap items-left gap-3">
              <label className="flex flex-col w-full gap-1 text-xs font-medium text-neutral-500">
                  Strategy
                <select
                  value={selectedAlgorithm}
                  onChange={(event) => setSelectedAlgorithm(event.target.value as SolverStrategy)}
                  disabled={isLoading}
                  className="w-full rounded-xl border border-neutral-200 bg-white fill-1 px-3 py-2 text-sm font-semibold text-neutral-800 shadow-soft transition focus:outline-none focus:ring-2 focus:ring-primary-100 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {ALGORITHMS.map(({ value, label }) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </div>
        </header>

        {error && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-100 bg-red-50/90 px-4 py-3 text-sm text-red-700">
            <span className="text-base">⚠️</span>
            <div className="flex-1">
              <p className="font-semibold">We couldn’t reach the solver.</p>
              <p className="text-red-600/80">{error}</p>
            </div>
            <button
              onClick={getSuggestion}
              className="text-xs font-semibold uppercase tracking-[0.2em] text-red-600 underline"
            >
              Retry
            </button>
          </div>
        )}

        <div className="mt-6 flex gap-3">
          <button
            onClick={getSuggestion}
            disabled={isLoading}
            className={`${BUTTON.secondary} flex-1 text-sm`}
          >
            {isLoading ? "Thinking..." : "Ask the agent"}
          </button>

          {hasSuggestion && (
            <button
              onClick={clearSuggestion}
              className={`${BUTTON.secondary} shrink-0 text-sm`}
            >
              Clear
            </button>
          )}
        </div>

        <footer className="mt-4 text-xs text-neutral-500">
          {statusMessage}
        </footer>
      </section>
    </div>
  );
}
