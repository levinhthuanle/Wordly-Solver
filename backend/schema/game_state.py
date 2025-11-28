"""Shared game state structures."""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class GuessState(BaseModel):
    """Represents a submitted guess and its feedback."""

    guess: str = Field(..., min_length=5, max_length=5)
    feedback: str = Field(..., pattern=r"^[012]{5}$")


class GameState(BaseModel):
    """Aggregated state for a game session."""

    history: List[GuessState] = Field(default_factory=list)
    remaining_candidates: int = Field(0, ge=0)
    solved: bool = Field(False, description="True when the puzzle is solved.")
    solution: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=5,
        description="Solved answer, when known.",
    )