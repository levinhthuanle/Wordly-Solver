from __future__ import annotations

from collections import Counter
from typing import Dict, List, Sequence

import numpy as np

from .base import Agent
from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse


class KBeamAgent(Agent):
    """Two-phase beam-search agent combining frequency and entropy heuristics."""

    def __init__(self, beam_width: int = 50) -> None:
        super().__init__()
        self.beam_width = beam_width
        self.first_guess = "ROATE"
        self._pattern_space = 3**5
        self._batch_size = 64

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(self, request: SolveRequest) -> SolveResponse:
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

        entropy_scores = self._batched_entropy_scores(beam, candidates)

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

    def _batched_entropy_scores(
        self,
        guesses: Sequence[str],
        candidates: Sequence[str],
    ) -> Dict[str, float]:
        if not guesses or not candidates:
            return {word: 0.0 for word in guesses}

        guess_indices = self._word_manager.words_to_indices([word.upper() for word in guesses])
        candidate_indices = self._word_manager.words_to_indices(
            [word.upper() for word in candidates]
        )

        scores: Dict[str, float] = {}
        for start in range(0, len(guesses), self._batch_size):
            chunk_words = guesses[start : start + self._batch_size]
            chunk_indices = guess_indices[start : start + self._batch_size]
            codes = self._word_manager.feedback_codes(chunk_indices, candidate_indices)
            entropies = self._entropy_from_codes(codes)
            for word, entropy in zip(chunk_words, entropies):
                scores[word] = float(entropy)

        return scores

    def _entropy_from_codes(self, codes: np.ndarray) -> np.ndarray:
        if codes.size == 0:
            return np.zeros(codes.shape[0])

        num_rows = codes.shape[0]
        offsets = (np.arange(num_rows, dtype=np.int64) * self._pattern_space)[:, None]
        flattened = codes.astype(np.int64, copy=False) + offsets
        hist = np.bincount(flattened.ravel(), minlength=num_rows * self._pattern_space).reshape(
            num_rows, self._pattern_space
        )
        hist = hist.astype(np.float64, copy=False)

        totals = hist.sum(axis=1, keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            probs = np.divide(hist, totals, out=np.zeros_like(hist), where=totals != 0)
            entropy = -np.sum(np.where(probs > 0, probs * np.log2(probs), 0.0), axis=1)
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
