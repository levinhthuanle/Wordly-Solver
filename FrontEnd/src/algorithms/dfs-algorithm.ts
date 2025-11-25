import { BaseAgent } from "./base-agent";
import { normalize } from "@/utils/game-utils";

/**
 * DFS (Depth-First Search) Algorithm
 * Systematic exploration with frequency-based scoring
 */
export class DFSAgent extends BaseAgent {
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

    // Find word with highest frequency score
    let bestWord = possibleWords[0];
    let bestScore = -1;

    // Limit search to avoid performance issues
    const searchSpace = possibleWords.slice(0, Math.min(100, possibleWords.length));

    for (const word of searchSpace) {
      const score = this.scoreWordFrequency(word, possibleWords);
      if (score > bestScore) {
        bestScore = score;
        bestWord = word;
      }
    }

    return bestWord;
  }
}
