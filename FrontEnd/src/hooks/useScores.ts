import { useState, useEffect } from "react";

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
        // Load from localStorage (backend no longer stores history)
        const savedScores = localStorage.getItem("wordly-scores");
        if (savedScores) {
          setScores(JSON.parse(savedScores));
        }
      } catch (err) {
        console.error("Error loading scores from localStorage:", err);
      } finally {
        setLoading(false);
      }
    };

    loadScores();
  }, []);

  return { scores, loading };
}

