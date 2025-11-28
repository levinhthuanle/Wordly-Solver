"""Pydantic models for autoplay simulation."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .solve_request import GuessFeedback, SolverStrategy
from .solve_response import AgentThought


class AutoplayRequest(BaseModel):
    """Parameters to run a fully automated solver simulation."""

    answer: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=5,
        description="Optional hidden answer; defaults to a random dictionary word.",
    )
    strategy: SolverStrategy = Field(
        default=SolverStrategy.ENTROPY,
        description="Agent strategy used during autoplay.",
    )
    max_attempts: int = Field(
        default=6,
        ge=1,
        le=10,
        description="Maximum number of guesses the bot will attempt.",
    )
    allow_repeats: bool = Field(
        default=False,
        description="Whether the bot may repeat previous guesses.",
    )


class AutoplayStep(BaseModel):
    """Single guess within the autoplay transcript."""

    guess: str = Field(..., min_length=5, max_length=5)
    feedback: str = Field(..., min_length=5, max_length=5)
    thoughts: List[AgentThought] = Field(default_factory=list)
    remaining_candidates: int = Field(
        0, ge=0, description="Candidates the agent believed remained after the guess."
    )


class AutoplayResponse(BaseModel):
    """Summary of the autoplay session."""

    answer: str = Field(..., min_length=5, max_length=5)
    solved: bool
    attempts_used: int = Field(..., ge=0)
    steps: List[AutoplayStep] = Field(default_factory=list)

