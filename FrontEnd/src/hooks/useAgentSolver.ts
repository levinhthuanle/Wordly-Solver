"use client";

import { useState, useRef } from "react";
import { useGameStore } from "@/stores/game-store";
import { WordlyAgentSolver } from "@/utils/agent-solver";
import { loadWords } from "@/utils/word-loader";

export function useAgentSolver() {
  const [isRunning, setIsRunning] = useState(false);
  const agentRef = useRef<WordlyAgentSolver | null>(null);
  
  const { 
    answer, 
    isGameOver, 
    submitAgentGuess, 
    setAgentPlaying,
    isAgentPlaying 
  } = useGameStore();

  const runAgent = async () => {
    if (isGameOver || isRunning) return;
    
    setIsRunning(true);
    setAgentPlaying(true);

    try {
      // Load word list
      const words = await loadWords();
      
      // Initialize agent
      if (!agentRef.current) {
        agentRef.current = new WordlyAgentSolver(words);
      } else {
        agentRef.current.reset();
      }

      // Run agent step by step
      let attempts = 0;
      const maxAttempts = 6;

      while (attempts < maxAttempts && !useGameStore.getState().isGameOver) {
        // Wait for previous animation to finish
        await new Promise(resolve => setTimeout(resolve, 2000));

        const guess = await agentRef.current.solveStep(answer);
        
        if (!guess) {
          console.error("Agent couldn't find a valid guess");
          break;
        }

        // Submit the guess
        submitAgentGuess(guess);
        attempts++;

        // Check if won
        if (useGameStore.getState().isWinner) {
          break;
        }
      }
    } catch (error) {
      console.error("Agent error:", error);
    } finally {
      setIsRunning(false);
      setAgentPlaying(false);
    }
  };

  const stopAgent = () => {
    setIsRunning(false);
    setAgentPlaying(false);
  };

  return {
    runAgent,
    stopAgent,
    isRunning,
    isAgentPlaying,
  };
}
