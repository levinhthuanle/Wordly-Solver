from __future__ import annotations

from pathlib import Path

from .base import Agent
from schema.solve_request import SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse

class RandomAgent(Agent):
    """Wordly solving agent that selects guesses at random."""

    def __init__(self):
        super().__init__() 

    def solve(self, request: SolveRequest) -> SolveResponse:
        """Produce the next guess recommendation for the given history."""
        import random

        parameters = request.parameters or SolveParameters()
        history = request.history

        candidates = self._apply_history(history)
        remaining = len(candidates)

        if remaining == 0:
            return SolveResponse(
                next_guess=None,
                suggestions=[],
                remaining_candidates=0,
                thoughts=[
                    AgentThought(
                        message="No candidates match the provided feedback history.",
                        score=None,
                    )
                ],
            )

        suggestions = random.sample(
            candidates,
            k=min(parameters.max_suggestions, len(candidates)),
        )
        next_guess = suggestions[0] if suggestions else None

        return SolveResponse(
            next_guess=next_guess,
            suggestions=suggestions,
            remaining_candidates=remaining,
            thoughts=[
                AgentThought(
                    message=f"Selected {next_guess} at random from {remaining} candidates.",
                    score=None,
                )
            ],
        )