import { BaseAgent } from "./base-agent";
import { normalize } from "@/utils/game-utils";

/**
 * Simulated Annealing Algorithm
 * Probabilistic acceptance of worse solutions to escape local optima
 */
export class SimulatedAnnealingAgent extends BaseAgent {
  constructor(wordList: string[]) {
    super(wordList.map(w => normalize(w)));
  }

  protected chooseBestGuess(possibleWords: string[]): string {
    // If only one word left, return it
    if (possibleWords.length === 1) {
      return possibleWords[0];
    }

    // First guess: use optimal starter
    if (this.currentGuesses.length === 0) {
      const starters = this.getOptimalStarters();
      for (const starter of starters) {
        if (possibleWords.includes(starter)) {
          return starter;
        }
      }
    }

    // Simulated Annealing parameters
    let temperature = 100.0;
    const coolingRate = 0.85;
    const minTemperature = 1.0;
    const maxIterations = 50;

    // Start from random word
    let currentWord = possibleWords[Math.floor(Math.random() * Math.min(10, possibleWords.length))];
    let currentScore = this.scoreWordEntropy(currentWord, possibleWords);
    let bestWord = currentWord;
    let bestScore = currentScore;

    let iterations = 0;

    while (temperature > minTemperature && iterations < maxIterations) {
      iterations++;

      // Get random neighbor
      const neighbors = this.getNeighbors(currentWord, possibleWords, 20);
      if (neighbors.length === 0) break;

      const neighbor = neighbors[Math.floor(Math.random() * neighbors.length)];
      const neighborScore = this.scoreWordEntropy(neighbor, possibleWords);

      // Calculate acceptance probability
      const delta = neighborScore - currentScore;
      const acceptanceProbability = delta > 0 ? 1 : Math.exp(delta / temperature);

      // Accept or reject based on probability
      if (Math.random() < acceptanceProbability) {
        currentWord = neighbor;
        currentScore = neighborScore;

        // Update best if improved
        if (currentScore > bestScore) {
          bestWord = currentWord;
          bestScore = currentScore;
        }
      }

      // Cool down temperature
      temperature *= coolingRate;
    }

    return bestWord;
  }

  /**
   * Get neighbors of a word (random sample from possible words)
   */
  private getNeighbors(word: string, possibleWords: string[], sampleSize: number): string[] {
    const neighbors: string[] = [];
    
    // Add random samples from possible words
    const shuffled = [...possibleWords].sort(() => Math.random() - 0.5);
    neighbors.push(...shuffled.slice(0, sampleSize));

    // Remove duplicates and the current word
    return Array.from(new Set(neighbors)).filter(w => w !== word);
  }
}
