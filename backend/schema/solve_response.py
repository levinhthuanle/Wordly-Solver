"""Response model for the Wordly solving agent."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AgentThought(BaseModel):
    """Optional reasoning step produced by the agent."""

    message: str = Field(..., description="Natural language description of the step")
    score: Optional[float] = Field(
        default=None,
        description="Optional numeric score (e.g., entropy) associated with the step.",
    )


class SolveResponse(BaseModel):
    """Structured agent response consumed by the frontend."""

    next_guess: Optional[str] = Field(
        default=None,
        description="Recommended next guess (upper-case 5 letters)",
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Alternative guesses sorted by preference (upper-case).",
    )
    remaining_candidates: int = Field(
        0, ge=0, description="Number of candidate answers remaining after filtering."
    )
    thoughts: List[AgentThought] = Field(
        default_factory=list,
        description="Optional stream of agent reasoning steps.",
    )



