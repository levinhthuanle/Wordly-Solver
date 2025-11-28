// types/types.ts
export type LetterState = "correct" | "present" | "absent" | "unused";

export type KeyboardState = Record<string, Exclude<LetterState, "unused"> | undefined>;

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

export type SolverStrategy = 'entropy' | 'random' | 'frequency' | 'better_entropy';

export interface AgentThought {
  message: string;
  score?: number | null;
}

export interface SolveHistoryEntry {
  guess: string;
  feedback: string;
}

export interface SolveRequest {
  history: SolveHistoryEntry[];
  strategy: SolverStrategy;
  maxSuggestions: number;
}

export type SolveRequestPayload = {
  history: SolveHistoryEntry[];
  parameters: {
    strategy: SolverStrategy;
    max_suggestions: number;
    allow_repeats: boolean;
  };
};

export type SolveResponsePayload = {
  next_guess?: string | null;
  suggestions?: string[];
  remaining_candidates?: number;
  thoughts?: AgentThought[];
};

export interface ValidateResponse {
  word: string;
  valid: boolean;
  message: string;
}

export interface AISuggestion {
  word: string;
  confidence: number;
  reasoning: string;
  remaining_count: number;
  alternatives: string[];
}