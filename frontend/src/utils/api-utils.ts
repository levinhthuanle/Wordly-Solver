/**
 * Modern API client for solver backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_SOLVER_API || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface AISuggestion {
  word: string;
  confidence: number;
  reasoning: string;
  remaining_count: number;
  algorithm: string;
}

export interface SolveRequest {
  guesses: string[];
  evaluations: string[][];
  algorithm: string;
}

export interface ValidateResponse {
  word: string;
  valid: boolean;
  message: string;
}

class SolverAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl.replace('/api', '')}/health`, {
        method: 'GET',
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  async getSuggestion(
    guesses: string[],
    evaluations: string[][],
    algorithm: string = 'dfs'
  ): Promise<AISuggestion> {
    const response = await fetch(`${this.baseUrl}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        guesses,
        evaluations,
        algorithm,
      } as SolveRequest),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get suggestion');
    }

    return response.json();
  }

  async validateWord(word: string): Promise<ValidateResponse> {
    const response = await fetch(`${this.baseUrl}/validate`, {
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

  async getAllWords(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/words/all`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch word list');
    }

    const data = await response.json();
    return data.words;
  }
}

export const solverAPI = new SolverAPI();
