import { BaseAgent } from "./base-agent";
import { normalize } from "@/utils/game-utils";

/**
 * Hill Climbing Algorithm
 * Greedy local search that always chooses the best neighbor
 */
export class HillClimbingAgent extends BaseAgent {
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

    // Hill Climbing: Start from random word, iteratively improve
    let currentWord = possibleWords[Math.floor(Math.random() * Math.min(10, possibleWords.length))];
    let currentScore = this.scoreWordEntropy(currentWord, possibleWords);
    let improved = true;

    const maxIterations = 20;
    let iterations = 0;

    while (improved && iterations < maxIterations) {
      improved = false;
      iterations++;

      // Check neighbors (random sample from possible words)
      const sampleSize = Math.min(30, possibleWords.length);
      const neighbors = this.getNeighbors(currentWord, possibleWords, sampleSize);

      for (const neighbor of neighbors) {
        const neighborScore = this.scoreWordEntropy(neighbor, possibleWords);
        if (neighborScore > currentScore) {
          currentWord = neighbor;
          currentScore = neighborScore;
          improved = true;
          break; // Take first improvement (greedy)
        }
      }
    }

    return currentWord;
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
