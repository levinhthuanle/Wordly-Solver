from __future__ import annotations

from typing import Iterable, List, Sequence, Set
from abc import ABC, abstractmethod
from word_manager.word_manager import wordlist

from schema.solve_request import GuessFeedback, SolveRequest
from schema.solve_response import SolveResponse


class Agent(ABC):
    """Interface for the Wordly solving agent."""

    def __init__(self) -> None:
        self.all_words: Set[str] = set(wordlist.words)
        self._word_manager = wordlist

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @abstractmethod
    def solve(self, request: SolveRequest) -> SolveResponse: ...

    def reset(self) -> None:
        """Reset any cached state (placeholder for future benchmark mode)."""

        # Agent currently does not maintain mutable state between requests.
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _apply_history(self, history: Sequence[GuessFeedback]) -> List[str]:
        candidates: Set[str] = set(self.all_words)
        for entry in history:
            guess = entry.guess.upper()
            feedback = entry.feedback
            candidates = self._filtered_candidates(candidates, guess, feedback)
        return sorted(candidates)

    def _filtered_candidates(
        self, candidates: Iterable[str], guess: str, feedback_pattern: str
    ) -> Set[str]:
        return {word for word in candidates if self._get_pattern(guess, word) == feedback_pattern}

    def _get_pattern(self, guess: str, target: str) -> str:
        guess = guess.upper()
        target = target.upper()
        return self._word_manager.get_feedback_pattern(guess, target)

    @staticmethod
    def compute_feedback(guess: str, target: str) -> str:
        """Compute feedback pattern for a given guess and target word."""
        guess = guess.upper()
        target = target.upper()
        pattern = []
        target_char_count = {}

        # First pass: identify correct positions (G)
        for g_char, t_char in zip(guess, target):
            if g_char == t_char:
                pattern.append("2")
            else:
                pattern.append(None)
                target_char_count[t_char] = target_char_count.get(t_char, 0) + 1

        # Second pass: identify present (Y) and absent (B)
        for i, g_char in enumerate(guess):
            if pattern[i] is None:
                if g_char in target_char_count and target_char_count[g_char] > 0:
                    pattern[i] = "1"
                    target_char_count[g_char] -= 1
                else:
                    pattern[i] = "0"

        return "".join(pattern)
