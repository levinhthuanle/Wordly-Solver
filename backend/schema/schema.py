"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional


class SolveRequest(BaseModel):
    """Request to get AI suggestion for next guess."""
    guesses: List[str] = Field(default_factory=list, description="Previous guesses")
    evaluations: List[List[str]] = Field(default_factory=list, description="Evaluation for each guess")
    algorithm: str = Field(default="dfs", description="Algorithm to use: dfs, hill-climbing, simulated-annealing")


class SolveResponse(BaseModel):
    """Response with AI suggestion compatible with AISuggestion flow."""
    word: str = Field(description="Suggested next word")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(description="Human-readable explanation")
    remaining_count: int = Field(description="Number of possible words remaining")
    algorithm: str = Field(description="Algorithm used")


class ValidateRequest(BaseModel):
    """Request to validate a word."""
    word: str = Field(min_length=5, max_length=5, description="5-letter word to validate")


class ValidateResponse(BaseModel):
    """Response for word validation."""
    word: str
    valid: bool
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    words_count: int
    timestamp: str
