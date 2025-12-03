from typing import Dict, List, Sequence

import numpy as np

from . import Agent
from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse


class EntropyAgent(Agent):
    """Wordly solving agent based on entropy scoring."""

    def __init__(self) -> None:
        super().__init__()
        self.first_guess = "ROATE"
        self._pattern_space = 3**5
        self._batch_size = 128

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

        entropy_scores = self._batched_entropy_scores(candidates, candidates)

        ranked = sorted(
            candidates,
            key=lambda word: entropy_scores[word],
            reverse=True,
        )

        if not parameters.allow_repeats:
            tried = {entry.guess.upper() for entry in history}
            ranked = [word for word in ranked if word not in tried] or ranked

        return ranked

    def _batched_entropy_scores(
        self,
        guesses: Sequence[str],
        candidates: Sequence[str],
    ) -> Dict[str, float]:
        guess_list = [word.upper() for word in guesses]
        candidate_list = [word.upper() for word in candidates]
        if not guess_list or not candidate_list:
            return {word: 0.0 for word in guess_list}

        guess_indices = self._word_manager.words_to_indices(guess_list)
        candidate_indices = self._word_manager.words_to_indices(candidate_list)

        scores: Dict[str, float] = {}
        for start in range(0, len(guess_list), self._batch_size):
            chunk_words = guess_list[start : start + self._batch_size]
            chunk_indices = guess_indices[start : start + self._batch_size]
            codes = self._word_manager.feedback_codes(chunk_indices, candidate_indices)
            entropies = self._entropy_from_codes(codes)
            for word, entropy in zip(chunk_words, entropies):
                scores[word] = entropy - self._duplicate_penalty(word)

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

    @staticmethod
    def _duplicate_penalty(word: str) -> float:
        unique_letters = len(set(word))
        if unique_letters < 5:
            return (5 - unique_letters) * 0.05
        return 0.0

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
