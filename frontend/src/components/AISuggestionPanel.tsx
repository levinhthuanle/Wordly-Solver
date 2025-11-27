"use client";

import { useAISuggestions } from "@/hooks/useAISuggestions";
import type { AlgorithmType } from "@/types/types";

const ALGORITHMS: { value: AlgorithmType; label: string }[] = [
  { value: 'dfs', label: 'DFS (Reliable)' },
  { value: 'hill-climbing', label: 'Hill Climbing (Fast)' },
  { value: 'simulated-annealing', label: 'Simulated Annealing' },
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

  return (
    <div className="mb-6 p-4 bg-slate-800 rounded-lg border border-slate-700">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-300">🤖 AI Assistant</h3>
        
        <select
          value={selectedAlgorithm}
          onChange={(e) => setSelectedAlgorithm(e.target.value as AlgorithmType)}
          className="px-2 py-1 text-xs bg-slate-700 text-slate-200 rounded border border-slate-600 focus:outline-none focus:border-blue-500"
          disabled={isLoading}
        >
          {ALGORITHMS.map(({ value, label }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {suggestion && !isLoading && (
        <div className="mb-3 p-3 bg-slate-700/50 rounded border border-slate-600">
          <div className="flex items-center justify-between mb-2">
            <span className="text-2xl font-bold text-green-400 tracking-wider">
              {suggestion.word}
            </span>
            <span className="text-xs text-slate-400">
              {Math.round(suggestion.confidence * 100)}% confident
            </span>
          </div>
          <p className="text-xs text-slate-300 mb-1">{suggestion.reasoning}</p>
          <p className="text-xs text-slate-500">
            {suggestion.remaining_count} word{suggestion.remaining_count !== 1 ? 's' : ''} remaining
          </p>
        </div>
      )}

      {error && (
        <div className="mb-3 p-2 bg-red-900/20 border border-red-500/50 rounded">
          <p className="text-xs text-red-400">{error}</p>
        </div>
      )}

      <div className="flex gap-2">
        <button
          onClick={getSuggestion}
          disabled={isLoading}
          className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white text-sm font-medium rounded transition-colors"
        >
          {isLoading ? '🤔 Thinking...' : '💡 Get Suggestion'}
        </button>
        
        {suggestion && (
          <button
            onClick={clearSuggestion}
            className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded transition-colors"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
