import { useEffect } from "react";
import { useGameStore } from "@/stores/game-store";
import { backendAPI } from "@/utils/backend-api";

export function useGameStats() {
  const { isGameOver, isWinner, guesses, score, answer, evaluations } = useGameStore();

  useEffect(() => {
    if (isGameOver) {
      const won = isWinner;
      const numGuesses = guesses.length;

      // Save to backend history
      backendAPI.saveGameHistory(
        answer,
        won,
        numGuesses,
        score,
        guesses,
        evaluations
      ).catch((err) => console.error("Failed to save to backend history:", err));

      // Also keep localStorage backup for offline access
      try {
        const existing = JSON.parse(
          localStorage.getItem("wordly-scores") || "[]"
        );
        existing.push({
          score,
          attempts: numGuesses,
          word: answer,
          date: new Date().toISOString(),
        });
        localStorage.setItem("wordly-scores", JSON.stringify(existing));
      } catch (err) {
        console.error("Failed to save score to localStorage:", err);
      }
    }
  }, [isGameOver, isWinner, guesses.length, score, answer, evaluations]);
}

