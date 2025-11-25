// API client for backend communication

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface BackendGuessResponse {
  guess: string;
  confidence: number;
  remaining_words: number;
}

export interface ValidateResponse {
  word: string;
  valid: boolean;
  message: string;
}

export interface WordStatsResponse {
  total_words: number;
  letter_frequency: Record<string, number>;
  sample_words: string[];
}

export class BackendAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Validate a word
   */
  async validateWord(word: string): Promise<ValidateResponse> {
    const response = await fetch(`${this.baseUrl}/api/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word }),
    });

    if (!response.ok) {
      throw new Error('Validation failed');
    }

    return response.json();
  }

  /**
   * Get next guess from agent solver
   */
  async solveNextGuess(
    guesses: string[],
    evaluations: string[][]
  ): Promise<BackendGuessResponse> {
    const response = await fetch(`${this.baseUrl}/api/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        guesses,
        evaluations,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Solver failed');
    }

    return response.json();
  }

  /**
   * Get word statistics
   */
  async getWordStats(): Promise<WordStatsResponse> {
    const response = await fetch(`${this.baseUrl}/api/words/stats`);

    if (!response.ok) {
      throw new Error('Failed to get word stats');
    }

    return response.json();
  }

  /**
   * Get random word
   */
  async getRandomWord(): Promise<{ word: string }> {
    const response = await fetch(`${this.baseUrl}/api/words/random`);

    if (!response.ok) {
      throw new Error('Failed to get random word');
    }

    return response.json();
  }

  /**
   * Get daily word
   */
  async getDailyWord(): Promise<{ word: string; date: string }> {
    const response = await fetch(`${this.baseUrl}/api/words/daily`);

    if (!response.ok) {
      throw new Error('Failed to get daily word');
    }

    return response.json();
  }
}

// Export singleton instance
export const backendAPI = new BackendAPI();
