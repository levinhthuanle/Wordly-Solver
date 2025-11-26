// API client for backend communication

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface BackendGuessResponse {
  guess: string;
  confidence: number;
  remaining_words: number;
  algorithm: string;
}

export interface AgentRunResponse {
  success: boolean;
  attempts: number;
  guesses: string[];
  evaluations: string[][];
  algorithm: string;
  message: string;
}

export interface GameHistoryRecord {
  id: number;
  word: string;
  won: boolean;
  attempts: number;
  score: number;
  guesses: string[];
  evaluations: string[][];
  date: string;
  user_id?: string;
}

export interface HistoryStatsResponse {
  total_games: number;
  wins: number;
  losses: number;
  win_rate: number;
  average_attempts: number;
  average_score: number;
  guess_distribution: Record<string, number>;
  current_streak: number;
  max_streak: number;
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
    evaluations: string[][],
    algorithm: string = 'dfs'
  ): Promise<BackendGuessResponse> {
    const response = await fetch(`${this.baseUrl}/api/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        guesses,
        evaluations,
        algorithm,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Solver failed');
    }

    return response.json();
  }

  /**
   * Run agent solver from start to finish
   */
  async runAgentGame(
    answer: string,
    algorithm: string = 'dfs',
    maxAttempts: number = 6
  ): Promise<AgentRunResponse> {
    const response = await fetch(`${this.baseUrl}/api/agent/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        answer,
        algorithm,
        max_attempts: maxAttempts,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Agent run failed');
    }

    return response.json();
  }

  /**
   * Save game to history
   */
  async saveGameHistory(
    word: string,
    won: boolean,
    attempts: number,
    score: number,
    guesses: string[],
    evaluations: string[][],
    userId?: string
  ): Promise<GameHistoryRecord> {
    const response = await fetch(`${this.baseUrl}/api/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        word,
        won,
        attempts,
        score,
        guesses,
        evaluations,
        user_id: userId,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to save game history');
    }

    return response.json();
  }

  /**
   * Get game history
   */
  async getGameHistory(
    userId?: string,
    limit?: number
  ): Promise<{ total: number; games: GameHistoryRecord[] }> {
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId);
    if (limit) params.append('limit', limit.toString());

    const url = `${this.baseUrl}/api/history${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('Failed to get game history');
    }

    return response.json();
  }

  /**
   * Get history statistics
   */
  async getHistoryStats(userId?: string): Promise<HistoryStatsResponse> {
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId);

    const url = `${this.baseUrl}/api/history/stats${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('Failed to get history statistics');
    }

    return response.json();
  }

  /**
   * Clear game history
   */
  async clearGameHistory(userId?: string): Promise<{ success: boolean; message: string }> {
    const params = new URLSearchParams();
    if (userId) params.append('user_id', userId);

    const url = `${this.baseUrl}/api/history${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to clear game history');
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
