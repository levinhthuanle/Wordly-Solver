import { LetterState } from "@/types/types";
import { evaluateGuess, normalize } from "./game-utils";

export interface GuessResult {
  word: string;
  evaluation: LetterState[];
}

export class WordlyAgentSolver {
  private wordList: string[];
  private currentGuesses: GuessResult[] = [];
  
  constructor(wordList: string[]) {
    this.wordList = wordList.map(w => normalize(w));
  }

  /**
   * DFS-based solver that finds the answer by systematically trying words
   * and filtering based on feedback
   */
  public async solveStep(answer: string): Promise<string | null> {
    // Filter possible words based on previous guesses
    let possibleWords = this.filterPossibleWords(this.wordList, this.currentGuesses);
    
    if (possibleWords.length === 0) {
      return null; // No valid words left
    }

    // Choose next word using DFS strategy
    const nextGuess = this.chooseBestGuess(possibleWords);
    
    // Simulate getting feedback
    const evaluation = evaluateGuess(answer, nextGuess);
    
    // Store this guess
    this.currentGuesses.push({
      word: nextGuess,
      evaluation
    });

    return nextGuess;
  }

  /**
   * Filter words that match all previous guess patterns
   */
  private filterPossibleWords(words: string[], guesses: GuessResult[]): string[] {
    return words.filter(word => {
      // Check if this word matches all previous guess patterns
      for (const guess of guesses) {
        if (!this.wordMatchesPattern(word, guess)) {
          return false;
        }
      }
      return true;
    });
  }

  /**
   * Check if a word matches the pattern from a previous guess
   */
  private wordMatchesPattern(word: string, guess: GuessResult): boolean {
    const { word: guessWord, evaluation } = guess;
    
    // Track letters we've seen
    const wordLetters = word.split('');
    const guessLetters = guessWord.split('');

    // First pass: Check "correct" positions
    for (let i = 0; i < guessLetters.length; i++) {
      if (evaluation[i] === 'correct') {
        if (wordLetters[i] !== guessLetters[i]) {
          return false;
        }
      }
    }

    // Second pass: Check "present" and "absent"
    for (let i = 0; i < guessLetters.length; i++) {
      const letter = guessLetters[i];
      
      if (evaluation[i] === 'present') {
        // Letter must be in word but not at this position
        if (wordLetters[i] === letter) {
          return false; // Same position
        }
        if (!wordLetters.includes(letter)) {
          return false; // Not in word at all
        }
      } else if (evaluation[i] === 'absent') {
        // Letter should not be in word (unless it's correct/present elsewhere)
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
   * DFS strategy: Choose word that eliminates most possibilities
   * Uses frequency analysis and position information
   */
  private chooseBestGuess(possibleWords: string[]): string {
    if (possibleWords.length === 1) {
      return possibleWords[0];
    }

    // If this is the first guess, use a word with common letters
    if (this.currentGuesses.length === 0) {
      const commonStarters = ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE'];
      for (const starter of commonStarters) {
        if (possibleWords.includes(starter)) {
          return starter;
        }
      }
    }

    // Score each word based on letter frequency and position
    let bestWord = possibleWords[0];
    let bestScore = -1;

    for (const word of possibleWords.slice(0, Math.min(100, possibleWords.length))) {
      const score = this.scoreWord(word, possibleWords);
      if (score > bestScore) {
        bestScore = score;
        bestWord = word;
      }
    }

    return bestWord;
  }

  /**
   * Score a word based on how much information it provides
   */
  private scoreWord(word: string, possibleWords: string[]): number {
    let score = 0;
    const letters = word.split('');
    
    // Count letter frequencies in remaining possible words
    const letterFreq: Record<string, number> = {};
    const positionFreq: Record<string, number> = {};
    
    for (const possibleWord of possibleWords) {
      for (let i = 0; i < possibleWord.length; i++) {
        const letter = possibleWord[i];
        letterFreq[letter] = (letterFreq[letter] || 0) + 1;
        positionFreq[`${i}-${letter}`] = (positionFreq[`${i}-${letter}`] || 0) + 1;
      }
    }

    // Score based on frequency
    const uniqueLetters = new Set(letters);
    for (const letter of uniqueLetters) {
      score += letterFreq[letter] || 0;
    }

    // Bonus for position frequency
    for (let i = 0; i < letters.length; i++) {
      score += (positionFreq[`${i}-${letters[i]}`] || 0) * 2;
    }

    return score;
  }

  public reset(): void {
    this.currentGuesses = [];
  }

  public getGuessHistory(): GuessResult[] {
    return [...this.currentGuesses];
  }
}
