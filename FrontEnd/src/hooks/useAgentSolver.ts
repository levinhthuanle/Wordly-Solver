"use client";

import { useState, useRef } from "react";
import { useGameStore } from "@/stores/game-store";
import { WordlyAgentSolver } from "@/utils/agent-solver";
import { loadWords } from "@/utils/word-loader";
import { backendAPI } from "@/utils/backend-api";

export function useAgentSolver() {
  const [isRunning, setIsRunning] = useState(false);
  const [useBackend, setUseBackend] = useState(true);
  const agentRef = useRef<WordlyAgentSolver | null>(null);
  
  const { 
    answer, 
    isGameOver, 
    submitAgentGuess, 
    setAgentPlaying,
    isAgentPlaying,
    guesses,
    evaluations 
  } = useGameStore();

  const runAgentBackend = async () => {
    try {
      let attempts = 0;
      const maxAttempts = 6;

      while (attempts < maxAttempts && !useGameStore.getState().isGameOver) {
        await new Promise(resolve => setTimeout(resolve, 2000));

        const currentGuesses = useGameStore.getState().guesses;
        const currentEvaluations = useGameStore.getState().evaluations;

        // Call backend API
        const result = await backendAPI.solveNextGuess(
          currentGuesses,
          currentEvaluations
        );

        if (!result.guess) {
          console.error("Backend couldn't find a valid guess");
          break;
        }

        console.log(`🤖 Agent guess: ${result.guess} (confidence: ${(result.confidence * 100).toFixed(1)}%, ${result.remaining_words} words left)`);

        submitAgentGuess(result.guess);
        attempts++;

        if (useGameStore.getState().isWinner) {
          break;
        }
      }
    } catch (error) {
      console.error("Backend agent error:", error);
      // Fallback to client-side solver
      console.log("Falling back to client-side solver...");
      await runAgentClientSide();
    }
  };

  const runAgentClientSide = async () => {
    try {
      const words = await loadWords();
      
      if (!agentRef.current) {
        agentRef.current = new WordlyAgentSolver(words);
      } else {
        agentRef.current.reset();
      }

      let attempts = 0;
      const maxAttempts = 6;

      while (attempts < maxAttempts && !useGameStore.getState().isGameOver) {
        await new Promise(resolve => setTimeout(resolve, 2000));

        const guess = await agentRef.current.solveStep(answer);
        
        if (!guess) {
          console.error("Agent couldn't find a valid guess");
          break;
        }

        console.log(`🤖 Agent guess (client-side): ${guess}`);

        submitAgentGuess(guess);
        attempts++;

        if (useGameStore.getState().isWinner) {
          break;
        }
      }
    } catch (error) {
      console.error("Client-side agent error:", error);
    }
  };

  const runAgent = async () => {
    if (isGameOver || isRunning) return;
    
    setIsRunning(true);
    setAgentPlaying(true);

    try {
      // Check if backend is available
      const isBackendHealthy = await backendAPI.healthCheck();
      
      if (isBackendHealthy && useBackend) {
        console.log("🚀 Using backend solver");
        await runAgentBackend();
      } else {
        console.log("💻 Using client-side solver");
        await runAgentClientSide();
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

  const toggleBackend = () => {
    setUseBackend(!useBackend);
  };

  return {
    runAgent,
    stopAgent,
    isRunning,
    isAgentPlaying,
    useBackend,
    toggleBackend,
  };
}
