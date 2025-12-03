"""
Systematic exploration with frequency-based scoring.
This algorithm uses letter and position frequency to choose the best guess.
"""

from pathlib import Path
from typing import List, Sequence
import math
from agent.base import Agent
from schema.solve_request import SolveRequest
from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse


class FrequencyAgent(Agent):
    """Wordly solving agent based on frequency scoring."""

    def __init__(self) -> None:
        super().__init__()
        self.first_guess = "TARES"

    """Agent implementation powering Wordly solving endpoints."""

    def solve(self, request: SolveRequest) -> SolveResponse:
        """Produce the next guess recommendation for the given history."""

        parameters = request.parameters or SolveParameters()
        history = request.history

        if not history:
            opener = self.first_guess
            return SolveResponse(
                next_guess=opener,
                suggestions=[opener][: parameters.max_suggestions],
                remaining_candidates=len(self.all_words),
                thoughts=[
                    AgentThought(
                        message="No prior guesses supplied; using default opener.",
                        score=None,
                    )
                ],
            )

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

        ranked = self._rank_candidates(candidates, history, parameters)
        suggestions = ranked[: parameters.max_suggestions]
        next_guess = suggestions[0] if suggestions else None

        return SolveResponse(
            next_guess=next_guess,
            suggestions=suggestions,
            remaining_candidates=remaining,
            thoughts=self._describe_decision(history, remaining, ranked[:3]),
        )

    def _rank_candidates(
        self,
        candidates: Sequence[str],
        history: Sequence[GuessFeedback],
        parameters: SolveParameters,
    ) -> List[str]:
        if len(candidates) <= 2:
            return list(candidates)

        frequency_scores = {
            candidate: self._calculate_frequency(candidate, candidates) for candidate in candidates
        }

        ranked = sorted(
            candidates,
            key=lambda word: frequency_scores[word],
            reverse=True,
        )

        if not parameters.allow_repeats:
            tried = {entry.guess.upper() for entry in history}
            ranked = [word for word in ranked if word not in tried] or ranked

        return ranked

    def _calculate_frequency(self, candidate: str, candidates: Sequence[str]) -> float:
        """Calculate frequency score - higher for more common letter positions."""
        letter_position_counts = [{} for _ in range(5)]
        total_candidates = len(candidates)

        # Count letter frequencies at each position
        for word in candidates:
            for i, letter in enumerate(word):
                letter_position_counts[i][letter] = letter_position_counts[i].get(letter, 0) + 1

        # Score based on how common each letter is at its position
        # Higher frequency = better guess (more likely to match)
        score = 0.0
        seen_letters = set()
        for i, letter in enumerate(candidate):
            frequency = letter_position_counts[i].get(letter, 0) / total_candidates
            score += frequency

            # Penalize duplicate letters
            if letter in seen_letters:
                score -= 0.1
            seen_letters.add(letter)

        return score

    def _describe_decision(
        self,
        history: Sequence[GuessFeedback],
        remaining_candidates: int,
        top_ranked: Sequence[str],
    ) -> List[AgentThought]:
        thoughts: List[AgentThought] = []

        if history:
            last = history[-1]
            thoughts.append(
                AgentThought(
                    message=(
                        f"Processed guess '{last.guess.upper()}' with feedback {last.feedback}."
                    ),
                    score=None,
                )
            )

        thoughts.append(
            AgentThought(
                message=f"{remaining_candidates} candidates remain after filtering.",
                score=float(remaining_candidates),
            )
        )

        if top_ranked:
            joined = ", ".join(top_ranked)
            thoughts.append(
                AgentThought(
                    message=f"Top recommendations: {joined}.",
                    score=None,
                )
            )

        return thoughts
