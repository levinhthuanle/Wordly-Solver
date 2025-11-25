/**
 * Agent Algorithms Module
 * 
 * This module provides different solving algorithms for the Wordly game.
 * Each algorithm implements the BaseAgent interface with its own strategy.
 */

export { BaseAgent } from './base-agent';
export type { GuessResult } from './base-agent';
export { DFSAgent } from './dfs-algorithm';
export { HillClimbingAgent } from './hill-climbing-algorithm';
export { SimulatedAnnealingAgent } from './simulated-annealing-algorithm';

// Re-export AlgorithmType from types
export type { AlgorithmType } from '@/types/types';

import { DFSAgent } from './dfs-algorithm';
import { HillClimbingAgent } from './hill-climbing-algorithm';
import { SimulatedAnnealingAgent } from './simulated-annealing-algorithm';
import { BaseAgent } from './base-agent';
import { AlgorithmType } from '@/types/types';

/**
 * Factory function to create an agent based on algorithm type
 * 
 * @param wordList - List of valid words
 * @param algorithm - Type of algorithm to use
 * @returns Instance of the selected algorithm agent
 */
export function createAgent(wordList: string[], algorithm: AlgorithmType): BaseAgent {
  switch (algorithm) {
    case 'dfs':
      return new DFSAgent(wordList);
    case 'hill-climbing':
      return new HillClimbingAgent(wordList);
    case 'simulated-annealing':
      return new SimulatedAnnealingAgent(wordList);
    default:
      console.warn(`Unknown algorithm: ${algorithm}, defaulting to DFS`);
      return new DFSAgent(wordList);
  }
}

/**
 * Get display name for algorithm
 */
export function getAlgorithmName(algorithm: AlgorithmType): string {
  switch (algorithm) {
    case 'dfs':
      return 'DFS (Depth-First Search)';
    case 'hill-climbing':
      return 'Hill Climbing';
    case 'simulated-annealing':
      return 'Simulated Annealing';
    default:
      return algorithm;
  }
}

/**
 * Get description for algorithm
 */
export function getAlgorithmDescription(algorithm: AlgorithmType): string {
  switch (algorithm) {
    case 'dfs':
      return 'Systematic exploration with frequency-based scoring. Guarantees finding a solution but may not be optimal.';
    case 'hill-climbing':
      return 'Greedy local search that always chooses the best neighbor. Fast but may get stuck in local optima.';
    case 'simulated-annealing':
      return 'Probabilistic algorithm that can escape local optima by accepting worse solutions with decreasing probability.';
    default:
      return '';
  }
}
