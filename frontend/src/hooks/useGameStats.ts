import { useEffect } from "react";
import { useGameStore } from "@/stores/game-store";

export function useGameStats() {
  const { isGameOver, isWinner, guesses, score, answer } = useGameStore();

  useEffect(() => {
    if (isGameOver) {
      const numGuesses = guesses.length;

      // Save to localStorage (backend no longer stores history)
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
  }, [isGameOver, isWinner, guesses.length, score, answer]);
}

