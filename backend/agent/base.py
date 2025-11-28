from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Sequence, Set
from abc import ABC, abstractmethod
from word_manager.word_manager import wordlist

from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest
from schema.solve_response import AgentThought, SolveResponse



class Agent(ABC):
    """Interface for the Wordly solving agent."""

    def __init__(self) -> None:
        self.all_words: Set[str] = set(wordlist.words)

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
        return {
            word
            for word in candidates
            if self._get_pattern(guess, word) == feedback_pattern
        }

    @staticmethod
    def _get_pattern(guess: str, target: str) -> str:
        guess = guess.upper()
        target = target.upper()

        result = ["0"] * len(guess)
        remaining: dict[str, int] = {}

        for char in target:
            remaining[char] = remaining.get(char, 0) + 1

        for idx, char in enumerate(guess):
            if char == target[idx]:
                result[idx] = "2"
                remaining[char] -= 1

        for idx, char in enumerate(guess):
            if result[idx] != "0":
                continue
            if remaining.get(char, 0) > 0:
                result[idx] = "1"
                remaining[char] -= 1

        return "".join(result)