"""Agent solver logic with lazy-loaded wordlist."""

import json
import os
from collections.abc import Mapping
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from numpy.lib.format import open_memmap


class WordListManager:
    """Lazy-loaded singleton for word list."""

    _instance: Optional["WordListManager"] = None
    _words: Optional[List[str]] = None
    _feedback: Optional["_FeedbackLookup"] = None
    _word_index: Optional[Dict[str, int]] = None
    _feedback_matrix: Optional[np.memmap] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_feedback(self) -> Dict[str, Dict[str, str]]:
        if self._feedback is None:
            self._ensure_feedback_matrix()
            self._feedback = _FeedbackLookup(self)
        return self._feedback

    def load_words(self) -> List[str]:
        """Load words from JSON file (cached after first load)."""
        if self._words is not None:
            return self._words

        base_dir = Path(__file__).resolve().parent
        data_path = base_dir / "wordlist.json"

        if not data_path.exists():
            # Fallback to old words.txt for migration
            txt_path = base_dir / "words.txt"
            if txt_path.exists():
                with open(txt_path, "r") as f:
                    self._words = [word.strip().upper() for word in f if len(word.strip()) == 5]
                print(f"Loaded {len(self._words)} words from legacy words.txt")
                return self._words
            raise FileNotFoundError("No wordlist found")

        with open(data_path, "r") as f:
            data = json.load(f)

        if isinstance(data, dict):
            payload = data.get("words", [])
        elif isinstance(data, list):
            payload = data
        else:  # pragma: no cover - safeguard for unexpected formats
            raise ValueError("Unsupported word list format")

        normalized: List[str] = []
        for entry in payload:
            if isinstance(entry, str):
                normalized.append(entry.strip().upper())
            elif isinstance(entry, dict) and "word" in entry:
                word = entry["word"]
                if isinstance(word, str):
                    normalized.append(word.strip().upper())

        if not normalized:
            raise ValueError("Word list file is empty or malformed")

        self._words = normalized

        # Build deterministic index for matrix lookups
        self._word_index = {word: idx for idx, word in enumerate(self._words)}

        print(f"✅ Loaded {len(self._words)} words from wordlist.json")
        return self._words

    @property
    def words(self) -> List[str]:
        """Get word list (loads if needed)."""
        return self.load_words()

    @property
    def feedback(self) -> Dict[str, Dict[str, str]]:
        """Get feedback patterns (loads if needed)."""
        return self.load_feedback()

    def is_valid(self, word: str) -> bool:
        """Check if word exists in dictionary."""
        return word.upper() in self.words

    def get_feedback_pattern(self, guess: str, target: str) -> str:
        """Return Wordle-style feedback pattern for the guess/target pair."""
        code = self.get_feedback_code(guess, target)
        return _code_to_pattern(code, len(guess))

    def get_feedback_code(self, guess: str, target: str) -> int:
        matrix = self._ensure_feedback_matrix()
        index = self._ensure_word_index()
        try:
            guess_idx = index[guess.upper()]
            target_idx = index[target.upper()]
        except KeyError as exc:  # pragma: no cover - invalid user input
            raise ValueError("Word not found in dictionary") from exc
        return int(matrix[guess_idx, target_idx])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_word_index(self) -> Dict[str, int]:
        if self._word_index is None:
            _ = self.words  # loads words and builds index
        if self._word_index is None:  # pragma: no cover - defensive
            raise RuntimeError("Word index failed to initialize")
        return self._word_index

    def _feedback_matrix_path(self) -> Path:
        return Path(__file__).resolve().parent / "feedback_matrix.npy"

    def _ensure_feedback_matrix(self) -> np.memmap:
        if self._feedback_matrix is not None:
            return self._feedback_matrix

        words = self.words
        word_count = len(words)
        matrix_path = self._feedback_matrix_path()

        if matrix_path.exists():
            self._feedback_matrix = open_memmap(
                matrix_path, mode="r", dtype=np.uint8, shape=(word_count, word_count)
            )
            print(f"✅ Loaded feedback matrix from {matrix_path.name}")
            return self._feedback_matrix

        max_workers = min(32, (os.cpu_count() or 4))
        print(f"⚙️ Generating feedback matrix for {word_count} words using {max_workers} workers...")
        matrix = open_memmap(matrix_path, mode="w+", dtype=np.uint8, shape=(word_count, word_count))

        with ProcessPoolExecutor(
            max_workers=max_workers,
            initializer=_feedback_worker_init,
            initargs=(words,),
        ) as executor:
            word_index = self._ensure_word_index()
            for guess, codes in executor.map(_feedback_worker_compute, words, chunksize=4):
                matrix[word_index[guess], :] = codes

        matrix.flush()
        del matrix  # close write handle
        print(f"✅ Stored feedback matrix at {matrix_path.name}")

        self._feedback_matrix = open_memmap(
            matrix_path, mode="r", dtype=np.uint8, shape=(word_count, word_count)
        )
        return self._feedback_matrix


# Global singleton
wordlist = WordListManager()


_WORKER_WORDS: List[str] = []


def _feedback_worker_init(words: List[str]) -> None:
    global _WORKER_WORDS
    _WORKER_WORDS = words


def _feedback_worker_compute(guess: str) -> tuple[str, List[int]]:
    guess = guess.upper()
    feedback_codes: List[int] = []
    for target in _WORKER_WORDS:
        pattern = _compute_pattern(guess, target)
        feedback_codes.append(_pattern_to_code(pattern))
    return guess, feedback_codes


def _compute_pattern(guess: str, target: str) -> str:
    result = ["0"] * len(guess)
    remaining: Dict[str, int] = {}

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


def _pattern_to_code(pattern: str) -> int:
    code = 0
    for char in pattern:
        code = code * 3 + int(char)
    return code


def _code_to_pattern(code: int, length: int) -> str:
    digits = ["0"] * length
    for idx in range(length - 1, -1, -1):
        digits[idx] = str(code % 3)
        code //= 3
    return "".join(digits)


class _FeedbackLookup(Mapping[str, "_FeedbackRow"]):
    def __init__(self, manager: WordListManager) -> None:
        self._manager = manager

    def __getitem__(self, guess: str) -> "_FeedbackRow":
        return _FeedbackRow(self._manager, guess)

    def __iter__(self):  # pragma: no cover - not used in hot path
        return iter(self._manager.words)

    def __len__(self) -> int:  # pragma: no cover - not used in hot path
        return len(self._manager.words)


class _FeedbackRow(Mapping[str, str]):
    def __init__(self, manager: WordListManager, guess: str) -> None:
        self._manager = manager
        self._guess = guess

    def __getitem__(self, target: str) -> str:
        return self._manager.get_feedback_pattern(self._guess, target)

    def __iter__(self):  # pragma: no cover
        return iter(self._manager.words)

    def __len__(self) -> int:  # pragma: no cover
        return len(self._manager.words)
