"use client";

import { useState } from "react";
import { useGameStore } from "@/stores/game-store";
import { solverAPI, type AISuggestion } from "@/utils/api-utils";
import type { AlgorithmType } from "@/types/types";

export function useAISuggestions() {
  const [suggestion, setSuggestion] = useState<AISuggestion | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<AlgorithmType>('dfs');
  
  const { guesses, evaluations, isGameOver } = useGameStore();

  const getSuggestion = async () => {
    if (isGameOver || isLoading) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const result = await solverAPI.getSuggestion(
        guesses,
        evaluations,
        selectedAlgorithm
      );
      
      setSuggestion(result);
      console.log(`🤖 AI Suggestion (${selectedAlgorithm}):`, result.word, `(${Math.round(result.confidence * 100)}% confidence)`);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get suggestion';
      setError(errorMessage);
      console.error("AI Suggestion error:", errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSuggestion = () => {
    setSuggestion(null);
    setError(null);
  };

  return {
    suggestion,
    isLoading,
    error,
    selectedAlgorithm,
    setSelectedAlgorithm,
    getSuggestion,
    clearSuggestion,
  };
}
