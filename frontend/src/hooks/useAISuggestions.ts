"use client";

import { Dispatch, SetStateAction, useCallback, useEffect, useRef, useState } from "react";
import { useGameStore } from "@/stores/game-store";
import type { SolverStrategy, LetterState } from "@/types/types";
import { solverAPI, type AISuggestion } from "@/utils/api-utils";

type UseAISuggestionsResult = {
  suggestion: AISuggestion | null;
  isLoading: boolean;
  error: string | null;
  selectedAlgorithm: SolverStrategy;
  setSelectedAlgorithm: Dispatch<SetStateAction<SolverStrategy>>;
  getSuggestion: () => Promise<void>;
  clearSuggestion: () => void;
};

type SuggestionRequest = {
  guesses: string[];
  evaluations: LetterState[][];
  algorithm: SolverStrategy;
  signal: AbortSignal;
};

const requestSuggestion = async ({
  guesses,
  evaluations,
  algorithm,
  signal,
}: SuggestionRequest) =>
  solverAPI.getSuggestion({ guesses, evaluations, algorithm, signal });

export const useAISuggestions = (): UseAISuggestionsResult => {
  const guesses = useGameStore((state) => state.guesses);
  const evaluations = useGameStore((state) => state.evaluations);
  const isGameOver = useGameStore((state) => state.isGameOver);

  const [suggestion, setSuggestion] = useState<AISuggestion | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<SolverStrategy>("entropy");
  const abortRef = useRef<AbortController | null>(null);

  const cancelInFlight = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort();
      abortRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => cancelInFlight();
  }, [cancelInFlight]);

  const getSuggestion = useCallback(async () => {
    if (isGameOver || isLoading) {
      return;
    }

    cancelInFlight();
    const controller = new AbortController();
    abortRef.current = controller;

    setIsLoading(true);
    setError(null);

    try {
      const result = await requestSuggestion({
        guesses,
        evaluations,
        algorithm: selectedAlgorithm,
        signal: controller.signal,
      });
      setSuggestion(result);
    } catch (err) {
      if (controller.signal.aborted) {
        return;
      }
      console.error("AI Suggestion error:", err);
      const message =
        err instanceof Error ? err.message : "Failed to get suggestion";
      setError(message);
    } finally {
      if (!controller.signal.aborted) {
        setIsLoading(false);
        abortRef.current = null;
      }
    }
  }, [cancelInFlight, evaluations, guesses, isGameOver, isLoading, selectedAlgorithm]);

  const clearSuggestion = useCallback(() => {
    cancelInFlight();
    setSuggestion(null);
    setError(null);
    setIsLoading(false);
  }, [cancelInFlight]);

  useEffect(() => {
    if (isGameOver) {
      clearSuggestion();
    }
  }, [clearSuggestion, isGameOver]);

  return {
    suggestion,
    isLoading,
    error,
    selectedAlgorithm,
    setSelectedAlgorithm,
    getSuggestion,
    clearSuggestion,
  };
};
