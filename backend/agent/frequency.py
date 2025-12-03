"""
Systematic exploration with frequency-based scoring.
This algorithm uses letter and position frequency to choose the best guess.
"""

from collections import Counter
from typing import Dict, List, Sequence

from agent.base import Agent
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

        position_counts = self._build_position_counts(candidates)
        total_candidates = len(candidates)
        frequency_scores = {
            candidate: self._score_candidate(candidate, position_counts, total_candidates)
            for candidate in candidates
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

    def _build_position_counts(self, candidates: Sequence[str]) -> List[Dict[str, int]]:
        counts: List[Dict[str, int]] = [Counter() for _ in range(5)]
        for word in candidates:
            for idx, letter in enumerate(word):
                counts[idx][letter] += 1
        return counts

    def _score_candidate(
        self,
        candidate: str,
        position_counts: Sequence[Dict[str, int]],
        total_candidates: int,
    ) -> float:
        """Score a word using precomputed position frequencies."""

        if total_candidates == 0:
            return 0.0

        score = 0.0
        seen_letters = set()
        for idx, letter in enumerate(candidate):
            letter_freq = position_counts[idx].get(letter, 0)
            score += letter_freq / total_candidates

            # Penalize duplicate letters to encourage broader coverage.
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
