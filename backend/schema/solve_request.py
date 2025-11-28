"""Request models for the Wordly solving agent."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class GuessFeedback(BaseModel):
    """Single guess entry with the encoded Wordle feedback pattern."""

    guess: str = Field(
        ..., min_length=5, max_length=5, description="Guessed word"
    )
    feedback: str = Field(
        ...,
        pattern=r"^[012]{5}$",
        description="Encoded feedback where 2=correct,1=present,0=absent",
    )


class SolverStrategy(str, Enum):
    """Enumeration of available solver strategies."""

    ENTROPY = "entropy"
    RANDOM = "random"

class SolveParameters(BaseModel):
    """Optional tuning parameters for the agent."""

    max_suggestions: int = Field(
        1,
        ge=1,
        le=5,
        description="Number of candidate suggestions to return (1-5).",
    )
    allow_repeats: bool = Field(
        False,
        description="Whether guesses already tried can be suggested again.",
    )
    strategy: SolverStrategy = Field(
        default=SolverStrategy.ENTROPY,
        description="Solver strategy used to rank candidate guesses.",
    )


class SolveRequest(BaseModel):
    """Payload describing prior guesses and optional agent parameters."""

    history: List[GuessFeedback] = Field(
        default_factory=list,
        description="Chronological list of previous guesses with feedback.",
    )
    parameters: Optional[SolveParameters] = Field(
        default=None,
        description="Optional solver tuning parameters.",
    )
