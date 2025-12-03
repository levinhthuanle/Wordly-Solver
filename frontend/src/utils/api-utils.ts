import type {
  AISuggestion,
  AutoplayRequestPayload,
  AutoplayResponse,
  LetterState,
  SolveHistoryEntry,
  SolveRequestPayload,
  SolveResponsePayload,
  SolverStrategy,
  ValidateResponse,
} from "@/types/types";

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_SOLVER_API ?? "http://localhost:8000/api"
).replace(/\/$/, "");

const LETTER_STATE_TO_PATTERN: Record<LetterState, "0" | "1" | "2"> = {
  correct: "2",
  present: "1",
  absent: "0",
  unused: "0",
};

const encodeRow = (row: LetterState[]): string =>
  row
    .map((state) => LETTER_STATE_TO_PATTERN[state] ?? "0")
    .join("");

const buildHistory = (
  guesses: string[],
  evaluations: LetterState[][]
): SolveHistoryEntry[] =>
  guesses
    .map((guess, index) => {
      const evalRow = evaluations[index];
      if (!evalRow || evalRow.length !== guess.length) {
        return null;
      }
      return {
        guess: guess.toUpperCase(),
        feedback: encodeRow(evalRow),
      } satisfies SolveHistoryEntry;
    })
    .filter((entry): entry is SolveHistoryEntry => entry !== null);

const estimateConfidence = (remaining?: number): number => {
  if (remaining === undefined || remaining === null || remaining <= 1) {
    return 0.97;
  }
  const normalized = 1 / Math.sqrt(Math.max(1, remaining));
  return Number(Math.min(0.95, Math.max(0.05, normalized)).toFixed(3));
};

const deriveReasoning = (
  thoughts: SolveResponsePayload["thoughts"],
  remaining: number,
  historyLength: number
): string => {
  const firstThought = thoughts?.find(
    (thought): thought is { message: string } =>
      typeof thought === "object" && thought !== null && "message" in thought
  );

  if (firstThought && typeof firstThought.message === "string") {
    return firstThought.message;
  }

  if (historyLength === 0) {
    return "Using the default opener to maximize information gain.";
  }

  if (remaining <= 1) {
    return "Only one candidate remains based on the feedback so far.";
  }

  return `${remaining} candidates remain after applying your feedback history.`;
};

class SolverAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl.replace("/api", "")}/health`, {
        method: "GET",
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  async requestAISuggestions(
    payload: SolveRequestPayload,
    signal?: AbortSignal
  ): Promise<SolveResponsePayload> {
    const response = await fetch(`${this.baseUrl}/solve`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal,
    });

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || "Agent request failed");
    }

    return response.json();
  }

  async getSuggestion(params: {
    guesses: string[];
    evaluations: LetterState[][];
    algorithm: SolverStrategy;
    maxSuggestions?: number;
    allowRepeats?: boolean;
    signal?: AbortSignal;
  }): Promise<AISuggestion> {
    const {
      guesses,
      evaluations,
      algorithm,
      maxSuggestions = 3,
      allowRepeats = false,
      signal,
    } = params;

    const history = buildHistory(guesses, evaluations);

    const payload: SolveRequestPayload = {
      history,
      parameters: {
        strategy: algorithm,
        max_suggestions: maxSuggestions,
        allow_repeats: allowRepeats,
      },
    };

    const response = await this.requestAISuggestions(payload, signal);
    
    console.log("Solver response:", response);

    const remaining =
      typeof response.remaining_candidates === "number"
        ? response.remaining_candidates
        : response.suggestions?.length ?? 0;

    const reasoning = deriveReasoning(response.thoughts, remaining, history.length);

    const nextWord = response.next_guess ?? response.suggestions?.[0];
    if (!nextWord) {
      throw new Error(reasoning || "Solver did not return a suggestion");
    }

    return {
      word: nextWord,
      confidence: estimateConfidence(remaining),
      reasoning,
      remaining_count: remaining,
      alternatives: (response.suggestions ?? []).filter((word) => word !== nextWord),
    } satisfies AISuggestion;
  }

  async validateWord(word: string): Promise<ValidateResponse> {
    const response = await fetch(`${this.baseUrl}/validate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ word }),
    });

    if (!response.ok) {
      throw new Error("Validation failed");
    }

    return response.json();
  }

  async getAllWords(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/words/all`);

    if (!response.ok) {
      throw new Error("Failed to fetch word list");
    }

    const data = await response.json();
    return data.words;
  }

  async runAutoplay(payload: AutoplayRequestPayload): Promise<AutoplayResponse> {
    const response = await fetch(`${this.baseUrl}/autoplay`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || "Autoplay failed");
    }

    return response.json();
  }
}

export const solverAPI = new SolverAPI();
export type { AISuggestion };