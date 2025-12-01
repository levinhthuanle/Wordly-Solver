from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Sequence

from .base import Agent
from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse


class KBeamAgent(Agent):
    """Two-phase beam-search agent combining frequency and entropy heuristics."""

    def __init__(self) -> None:
        super().__init__()
        self.beam_width = 50

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(self, request: SolveRequest) -> SolveResponse:
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
                        message="No candidate answers remain for the supplied feedback.",
                        score=None,
                    )
                ],
            )

        ranked = self._rank_with_beam(candidates, history, parameters)
        suggestions = ranked[: parameters.max_suggestions]
        next_guess = suggestions[0] if suggestions else None

        return SolveResponse(
            next_guess=next_guess,
            suggestions=suggestions,
            remaining_candidates=remaining,
            thoughts=self._describe_decision(history, remaining, ranked[:3], candidates),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _rank_with_beam(
        self,
        candidates: Sequence[str],
        history: Sequence[GuessFeedback],
        parameters: SolveParameters,
    ) -> List[str]:
        if len(candidates) <= 2:
            return list(candidates)

        beam_width = min(self.beam_width, len(self.all_words))
        frequency_scores = self._letter_frequency_scores(candidates)

        ordered_by_frequency = sorted(
            self.all_words,
            key=lambda word: frequency_scores[word],
            reverse=True,
        )
        beam = ordered_by_frequency[:beam_width]

        entropy_scores: Dict[str, float] = {
            word: self._calculate_entropy(word, candidates) for word in beam
        }

        ranked = sorted(
            beam,
            key=lambda word: entropy_scores[word],
            reverse=True,
        )

        if not parameters.allow_repeats:
            tried = {entry.guess.upper() for entry in history}
            filtered = [word for word in ranked if word not in tried]
            if filtered:
                ranked = filtered

        return ranked

    def _letter_frequency_scores(self, candidates: Sequence[str]) -> Dict[str, float]:
        letter_counts: Counter[str] = Counter()
        for word in candidates:
            letter_counts.update(set(word))

        scores: Dict[str, float] = {}
        for word in self.all_words:
            unique_letters = set(word)
            scores[word] = sum(letter_counts.get(letter, 0) for letter in unique_letters)
        return scores

    def _calculate_entropy(self, guess: str, candidates: Sequence[str]) -> float:
        pattern_counts: Dict[str, int] = {}
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
        candidates: Sequence[str],
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
                message=f"Phase 1 (frequency) reduced search to top {self.beam_width} of {len(self.all_words)} words.",
                score=float(min(self.beam_width, len(self.all_words))),
            )
        )

        if top_ranked:
            thoughts.append(
                AgentThought(
                    message=f"Phase 2 entropy favors: {', '.join(top_ranked)}.",
                    score=None,
                )
            )

        thoughts.append(
            AgentThought(
                message=f"{remaining_candidates} candidate answers remain after filtering.",
                score=float(remaining_candidates),
            )
        )

        return thoughts
