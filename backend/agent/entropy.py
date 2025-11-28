from . import Agent
import math
from pathlib import Path
from typing import List, Sequence
from ..schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from ..schema.solve_response import AgentThought, SolveResponse


class EntropyAgent(Agent):
    """Wordly solving agent based on entropy scoring."""

    def __init__(self) -> None:
        super().__init__()
        self.first_guess = "ROATE"
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

        entropy_scores = {
            candidate: self._calculate_entropy(candidate, candidates)
            for candidate in candidates
        }

        ranked = sorted(
            candidates,
            key=lambda word: entropy_scores[word],
            reverse=True,
        )

        if not parameters.allow_repeats:
            tried = {entry.guess.upper() for entry in history}
            ranked = [word for word in ranked if word not in tried] or ranked

        return ranked

    def _calculate_entropy(self, guess: str, candidates: Sequence[str]) -> float:
        pattern_counts: dict[str, int] = {}
        for target in candidates:
            pattern = self._get_pattern(guess, target)
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        total = len(candidates)
        entropy = 0.0
        for count in pattern_counts.values():
            probability = count / total
            entropy -= probability * math.log2(probability)
        return entropy

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
