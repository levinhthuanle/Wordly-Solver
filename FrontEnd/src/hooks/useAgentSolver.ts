"use client";

import { useState } from "react";
import { useGameStore } from "@/stores/game-store";
import { AlgorithmType } from "@/types/types";
import { backendAPI } from "@/utils/backend-api";

export function useAgentSolver() {
  const [isRunning, setIsRunning] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<AlgorithmType>('dfs');
  
  const { 
    answer, 
    isGameOver, 
    submitAgentGuess, 
    setAgentPlaying,
    isAgentPlaying,
  } = useGameStore();

  const runAgent = async () => {
    if (isGameOver || isRunning) return;
    
    setIsRunning(true);
    setAgentPlaying(true);

    try {
      // Check if backend is available
      const isBackendHealthy = await backendAPI.healthCheck();
      
      if (!isBackendHealthy) {
        console.error("❌ Backend is not available");
        setIsRunning(false);
        setAgentPlaying(false);
        return;
      }

      console.log(`🚀 Running agent with ${selectedAlgorithm.toUpperCase()} algorithm`);
      
      // Call backend to run full agent game
      const result = await backendAPI.runAgentGame(answer, selectedAlgorithm, 6);
      
      console.log(`📊 Agent result: ${result.message}`);
      
      // Submit each guess with delay for animation
      for (let i = 0; i < result.guesses.length; i++) {
        if (i > 0) {
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
        
        const guess = result.guesses[i];
        console.log(`🤖 Agent guess ${i + 1}: ${guess}`);
        
        submitAgentGuess(guess);
        
        // Check if game is already over
        if (useGameStore.getState().isGameOver) {
          break;
        }
      }
      
      if (result.success) {
        console.log(`✅ Agent solved in ${result.attempts} attempts!`);
      } else {
        console.log(`❌ Agent failed to solve`);
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
    selectedAlgorithm,
    setSelectedAlgorithm,
  };
}
