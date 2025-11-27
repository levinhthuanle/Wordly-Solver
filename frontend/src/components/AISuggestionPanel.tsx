"use client";

import { BUTTON } from "@/constants/constants";
import { useAISuggestions } from "@/hooks/useAISuggestions";
import type { AlgorithmType } from "@/types/types";

const ALGORITHMS: { value: AlgorithmType; label: string }[] = [
  { value: "dfs", label: "DFS (Reliable)" },
  { value: "hill-climbing", label: "Hill Climbing (Fast)" },
  { value: "simulated-annealing", label: "Simulated Annealing" },
];

export function AISuggestionPanel() {
  const {
    suggestion,
    isLoading,
    error,
    selectedAlgorithm,
    setSelectedAlgorithm,
    getSuggestion,
    clearSuggestion,
  } = useAISuggestions();

  const hasSuggestion = Boolean(suggestion) && !isLoading;

  return (
    <section className="mt-8 w-full max-w-md rounded-2xl bg-white/80 p-6 shadow-soft ring-1 ring-neutral-200/70 backdrop-blur">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
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
        <label className="flex flex-col gap-1 text-xs font-medium text-neutral-500">
          Strategy
          <select
            value={selectedAlgorithm}
            onChange={(event) => setSelectedAlgorithm(event.target.value as AlgorithmType)}
            disabled={isLoading}
            className="rounded-xl border border-neutral-200 bg-white px-4 py-2 text-sm font-semibold text-neutral-800 shadow-soft transition focus:outline-none focus:ring-2 focus:ring-primary-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {ALGORITHMS.map(({ value, label }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </header>

      <div className="mt-6 space-y-4">
        {error && (
          <div className="rounded-2xl border border-red-100 bg-red-50/80 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        {hasSuggestion && suggestion && (
          <div className="rounded-2xl border border-primary-100 bg-gradient-to-br from-primary-50 to-white px-5 py-4 shadow-inner">
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
        )}

        {!error && !hasSuggestion && (
          <div className="rounded-2xl border border-dashed border-neutral-200 bg-neutral-50/80 px-5 py-4 text-sm text-neutral-500">
            {isLoading
              ? "Crunching possibilities…"
              : "Request a suggestion once you have at least one guess."}
          </div>
        )}
      </div>

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

      <footer className="mt-4 text-xs text-neutral-400">
        {isLoading
          ? "Analyzing your previous guesses"
          : hasSuggestion
          ? "Tap Clear to try a different strategy"
          : "Select a strategy to begin"}
      </footer>
    </section>
  );
}
