import { useState, useEffect } from "react";
import { backendAPI } from "@/utils/backend-api";

export type ScoreData = {
  score: number;
  date: string;
  attempts: number;
  word: string;
};

export function useScores() {
  const [scores, setScores] = useState<ScoreData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadScores = async () => {
      try {
        // Try to load from backend first
        const backendHealthy = await backendAPI.healthCheck();
        
        if (backendHealthy) {
          const historyData = await backendAPI.getGameHistory(undefined, 100);
          const formattedScores = historyData.games.map(game => ({
            score: game.score,
            date: game.date,
            attempts: game.attempts,
            word: game.word,
          }));
          setScores(formattedScores);
        } else {
          // Fallback to localStorage
          const savedScores = localStorage.getItem("wordly-scores");
          if (savedScores) {
            setScores(JSON.parse(savedScores));
          }
        }
      } catch (error) {
        console.error("Error loading scores from backend, using localStorage:", error);
        // Fallback to localStorage on error
        try {
          const savedScores = localStorage.getItem("wordly-scores");
          if (savedScores) {
            setScores(JSON.parse(savedScores));
          }
        } catch (err) {
          console.error("Error loading scores from localStorage:", err);
        }
      } finally {
        setLoading(false);
      }
    };

    loadScores();
  }, []);

  return { scores, loading };
}

