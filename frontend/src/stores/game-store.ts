"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { GAME } from "@/constants/constants";
import { AutoplayStep, LetterState, KeyboardState } from "@/types/types";
import {
  normalize,
  getDailyAnswer,
  getRandomAnswer,
  evaluateGuess,
  mergeKeyboardState,
  isValidWord,
} from "@/utils/game-utils";

type GameMode = "daily" | "random";

const FEEDBACK_TO_STATE: Record<string, LetterState> = {
  "2": "correct",
  "1": "present",
  "0": "absent",
};

const feedbackToStates = (feedback: string): LetterState[] =>
  feedback.split("").map((digit) => FEEDBACK_TO_STATE[digit] ?? "absent");

export interface GameStoreState {
  // Core game state
  answer: string;
  guesses: string[]; // past submitted guesses
  evaluations: LetterState[][]; // per-guess evaluations
  currentGuess: string;
  currentRow: number;
  boardRows: number;
  isRevealing: boolean;
  isGameOver: boolean;
  isWinner: boolean;
  invalidGuess: boolean;

  // Meta
  mode: GameMode;
  solutionId: string; // YYYY-MM-DD for daily or random seed id
  keyboard: KeyboardState; // letter -> best-known state
  score: number; // simple cumulative score like existing app
  
  // UI State
  isKeyboardVisible: boolean;
  isAutoplaying: boolean;
  syncAutoplayProgress: (params: {
    answer: string;
    steps: AutoplayStep[];
    uptoIndex: number;
  }) => void;
  stopAutoplayMode: () => void;
  applySuggestedGuess: (word: string) => void;
  
  // Actions
  startNewGame: (mode?: GameMode) => void;
  handleKey: (key: string) => void;
  addLetter: (letter: string) => void;
  removeLetter: () => void;
  submitGuess: () => void;
  resetInvalid: () => void;
  setKeyboardVisible: (visible: boolean) => void;
}

export const useGameStore = create<GameStoreState>()(
  persist(
    (set, get) => ({
      answer: "",
      guesses: [],
      evaluations: [],
      currentGuess: "",
      currentRow: 0,
      boardRows: GAME.MAX_ATTEMPTS,
      isRevealing: false,
      isGameOver: false,
      isWinner: false,
      invalidGuess: false,
      mode: "random",
      solutionId: "",
      keyboard: {},
      score: 0,
      isKeyboardVisible: true,
      isAutoplaying: false,

      startNewGame: async (mode) => {
        const desiredMode = mode ?? get().mode ?? "random";
        const { answer, id } =
          desiredMode === "daily" ? await getDailyAnswer() : await getRandomAnswer();
        set({
          answer,
          solutionId: id,
          mode: desiredMode,
          guesses: [],
          evaluations: [],
          currentGuess: "",
          currentRow: 0,
          isRevealing: false,
          isGameOver: false,
          isWinner: false,
          invalidGuess: false,
          keyboard: {},
          isAutoplaying: false,
        });
      },

      addLetter: (letter) => {
        const { currentGuess, isGameOver, isAutoplaying } = get();
        if (isGameOver || isAutoplaying) return;
        if (!/^[a-zA-Z]$/.test(letter)) return;
        if (currentGuess.length >= GAME.WORD_LENGTH) return;
        set({
          currentGuess: (currentGuess + normalize(letter)).slice(
            0,
            GAME.WORD_LENGTH
          ),
          invalidGuess: false,
        });
      },

      removeLetter: () => {
        const { currentGuess, isGameOver, isAutoplaying } = get();
        if (isGameOver || isAutoplaying) return;
        if (currentGuess.length === 0) return;
        set({ currentGuess: currentGuess.slice(0, -1), invalidGuess: false });
      },

      submitGuess: () => {
        const { currentGuess, answer, guesses, isGameOver, isAutoplaying } = get();
        if (isGameOver || isAutoplaying) return;
        if (currentGuess.length !== GAME.WORD_LENGTH) {
          set({ invalidGuess: true });
          return;
        }

        const guess = normalize(currentGuess);

        // Strict validation: block guesses that are not in the dictionary
        const isValid = isValidWord(guess);
        if (!isValid) {
          console.warn(`❌ "${guess}" is not in the dictionary.`);
          set({ invalidGuess: true });
          return;
        }

        const evals = evaluateGuess(answer, guess);
        const nextGuesses = [...guesses, guess];
        const nextEvaluations = [...get().evaluations, evals];
        const isWinner = evals.every((s) => s === "correct");
        const isLast = nextGuesses.length >= GAME.MAX_ATTEMPTS;
        const gameOver = isWinner || isLast;
        const addedScore = isWinner
          ? GAME.POINTS_PER_ATTEMPT * (GAME.MAX_ATTEMPTS - nextGuesses.length)
          : 0;

        set({
          guesses: nextGuesses,
          evaluations: nextEvaluations,
          currentGuess: "",
          currentRow: get().currentRow + 1,
          isRevealing: true,
          isWinner,
          isGameOver: gameOver,
          invalidGuess: false,
          keyboard: mergeKeyboardState(get().keyboard, guess, evals),
          score: get().score + addedScore,
        });

        // End reveal after animation duration
        const revealMs = (GAME.REVEAL_TIME_MS || 350) * GAME.WORD_LENGTH;
        setTimeout(() => {
          // Avoid toggling if a new game started
          if (get().guesses.length === nextGuesses.length) {
            set({ isRevealing: false });
          }
        }, revealMs);
      },

      handleKey: (key) => {
        if (get().isAutoplaying) {
          return;
        }
        if (key === "Enter") {
          get().submitGuess();
          return;
        }
        if (key === "Backspace" || key === "Delete") {
          get().removeLetter();
          return;
        }
        if (/^[a-zA-Z]$/.test(key)) {
          get().addLetter(key);
        }
      },

      resetInvalid: () => set({ invalidGuess: false }),

      setKeyboardVisible: (visible: boolean) => set({ isKeyboardVisible: visible }),

      syncAutoplayProgress: ({ answer, steps, uptoIndex }) => {
        if (!steps.length) {
          set({
            answer: normalize(answer),
            guesses: [],
            evaluations: [],
            currentGuess: "",
            currentRow: 0,
            boardRows: GAME.MAX_ATTEMPTS,
            boardRows: GAME.MAX_ATTEMPTS,
            isRevealing: false,
            isWinner: false,
            isGameOver: false,
            invalidGuess: false,
            keyboard: {},
            isAutoplaying: true,
          });
          return;
        }

        const effectiveIndex = Math.min(uptoIndex, steps.length - 1);
        const visibleSteps =
          effectiveIndex >= 0 ? steps.slice(0, effectiveIndex + 1) : [];

        const guesses = visibleSteps.map((step) => normalize(step.guess));
        const evaluations = visibleSteps.map((step) => feedbackToStates(step.feedback));

        let keyboard: KeyboardState = {};
        guesses.forEach((guess, idx) => {
          keyboard = mergeKeyboardState(keyboard, guess, evaluations[idx]);
        });

        const attemptsUsed = guesses.length;
        const plannedRows = Math.max(GAME.MAX_ATTEMPTS, steps.length);

        set({
          answer: normalize(answer),
          guesses,
          evaluations,
          currentGuess: "",
          currentRow: attemptsUsed,
          boardRows: plannedRows,
          isRevealing: false,
          isWinner: false,
          isGameOver: false,
          invalidGuess: false,
          keyboard,
          isAutoplaying: true,
        });
      },

      stopAutoplayMode: () => set({ isAutoplaying: false }),

      applySuggestedGuess: (word) => {
        const { isGameOver, isAutoplaying } = get();
        if (isGameOver || isAutoplaying) {
          return;
        }

        const normalized = normalize(word).slice(0, GAME.WORD_LENGTH);
        if (!normalized) {
          return;
        }

        set({ currentGuess: normalized, invalidGuess: false });
      },
    }),
    {
      name: "wordly-game", // persist basic game meta and score, not guesses
      partialize: (state) => ({
        mode: state.mode,
        solutionId: state.solutionId,
        score: state.score,
      }),
    }
  )
);
