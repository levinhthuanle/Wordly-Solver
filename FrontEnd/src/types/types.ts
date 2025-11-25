// types/types.ts
export type LetterState = "correct" | "present" | "absent" | "unused";

export type KeyboardState = Record<string, Exclude<LetterState, "unused"> | undefined>;

export type AlgorithmType = 'dfs' | 'hill-climbing' | 'simulated-annealing';

export interface WordEntry {
  word: string;
}

export interface GameState {
  wordToGuess: string;
  currentGuess: string;
  attempts: string[];
  isWinner: boolean;
  gameOver: boolean;
  score: number;
  currentRow: number;
  isRevealing: boolean;
  invalidGuess?: boolean;
}

export interface GameEndState {
  isWinner: boolean;
  message: string;
}
