import { LetterState } from "@/types/types";
import { evaluateGuess } from "@/utils/game-utils";

export interface GuessResult {
  word: string;
  evaluation: LetterState[];
}

/**
 * Abstract base class for all Wordly solving algorithms
 */
export abstract class BaseAgent {
  protected wordList: string[];
  protected currentGuesses: GuessResult[] = [];
  
  constructor(wordList: string[]) {
    this.wordList = wordList;
  }

  /**
   * Main method to get the next guess
   */
  public async solveStep(answer: string): Promise<string | null> {
    const possibleWords = this.filterPossibleWords(this.wordList, this.currentGuesses);
    
    if (possibleWords.length === 0) {
      return null;
    }

    const nextGuess = await this.chooseBestGuess(possibleWords);
    const evaluation = evaluateGuess(answer, nextGuess);
    
    this.currentGuesses.push({
      word: nextGuess,
      evaluation
    });

    return nextGuess;
  }

  /**
   * Abstract method that each algorithm must implement
   */
  protected abstract chooseBestGuess(possibleWords: string[]): Promise<string> | string;

  /**
   * Filter words that match all previous guess patterns
   */
  protected filterPossibleWords(words: string[], guesses: GuessResult[]): string[] {
    return words.filter(word => {
      for (const guess of guesses) {
        if (!this.wordMatchesPattern(word, guess)) {
          return false;
        }
      }
      return true;
    });
  }

  /**
   * Check if a word matches a guess pattern
   */
  protected wordMatchesPattern(word: string, guess: GuessResult): boolean {
    const { word: guessWord, evaluation } = guess;
    const wordLetters = word.split('');
    const guessLetters = guessWord.split('');

    // Check correct positions
    for (let i = 0; i < guessLetters.length; i++) {
      if (evaluation[i] === 'correct') {
        if (wordLetters[i] !== guessLetters[i]) {
          return false;
        }
      }
    }

    // Check present and absent
    for (let i = 0; i < guessLetters.length; i++) {
      const letter = guessLetters[i];
      
      if (evaluation[i] === 'present') {
        if (wordLetters[i] === letter) {
          return false;
        }
        if (!wordLetters.includes(letter)) {
          return false;
        }
      } else if (evaluation[i] === 'absent') {
        const letterHasCorrectOrPresent = evaluation.some((state, idx) => 
          guessLetters[idx] === letter && (state === 'correct' || state === 'present')
        );
        
        if (!letterHasCorrectOrPresent && wordLetters.includes(letter)) {
          return false;
        }
      }
    }

    return true;
  }

  /**
   * Score word based on letter frequency
   */
  protected scoreWordFrequency(word: string, possibleWords: string[]): number {
    let score = 0;
    const letters = word.split('');
    
    const letterFreq: Record<string, number> = {};
    const positionFreq: Record<string, number> = {};
    
    for (const possibleWord of possibleWords) {
      for (let i = 0; i < possibleWord.length; i++) {
        const letter = possibleWord[i];
        letterFreq[letter] = (letterFreq[letter] || 0) + 1;
        positionFreq[`${i}-${letter}`] = (positionFreq[`${i}-${letter}`] || 0) + 1;
      }
    }

    const uniqueLetters = new Set(letters);
    for (const letter of uniqueLetters) {
      score += letterFreq[letter] || 0;
    }

    for (let i = 0; i < letters.length; i++) {
      score += (positionFreq[`${i}-${letters[i]}`] || 0) * 2;
    }

    return score;
  }

  /**
   * Score word based on entropy (information gain)
   */
  protected scoreWordEntropy(word: string, possibleWords: string[]): number {
    if (possibleWords.length <= 1) return 0;

    const patterns: Map<string, number> = new Map();

    for (const candidate of possibleWords.slice(0, Math.min(200, possibleWords.length))) {
      const evaluation = this.simulateEvaluation(word, candidate);
      const patternKey = evaluation.join(',');
      patterns.set(patternKey, (patterns.get(patternKey) || 0) + 1);
    }

    let entropy = 0;
    const total = possibleWords.length;

    for (const count of patterns.values()) {
      const probability = count / total;
      if (probability > 0) {
        entropy -= probability * Math.log2(probability);
      }
    }

    return entropy;
  }

  /**
   * Simulate evaluation for entropy calculation
   */
  protected simulateEvaluation(guess: string, answer: string): LetterState[] {
    const result: LetterState[] = Array(5).fill('absent');
    const answerLetters = answer.split('');
    const guessLetters = guess.split('');
    const used = Array(5).fill(false);

    for (let i = 0; i < 5; i++) {
      if (guessLetters[i] === answerLetters[i]) {
        result[i] = 'correct';
        used[i] = true;
      }
    }

    for (let i = 0; i < 5; i++) {
      if (result[i] === 'correct') continue;
      
      for (let j = 0; j < 5; j++) {
        if (!used[j] && guessLetters[i] === answerLetters[j]) {
          result[i] = 'present';
          used[j] = true;
          break;
        }
      }
    }

    return result;
  }

  /**
   * Get optimal starting words
   */
  protected getOptimalStarters(): string[] {
    return ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE'];
  }

  /**
   * Reset agent state for new game
   */
  public reset(): void {
    this.currentGuesses = [];
  }

  /**
   * Get guess history
   */
  public getGuessHistory(): GuessResult[] {
    return [...this.currentGuesses];
  }
}
