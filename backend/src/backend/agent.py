"""Agent solver logic with lazy-loaded wordlist."""

import json
from pathlib import Path
from typing import List, Optional
from algorithms import create_agent
from algorithms.base_agent import GuessResult


class WordListManager:
    """Lazy-loaded singleton for word list."""
    
    _instance: Optional['WordListManager'] = None
    _words: Optional[List[str]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_words(self) -> List[str]:
        """Load words from JSON file (cached after first load)."""
        if self._words is not None:
            return self._words
        
        data_path = Path(__file__).parent / "data" / "wordlist.json"
        
        if not data_path.exists():
            # Fallback to old words.txt for migration
            txt_path = Path(__file__).parent.parent / "words.txt"
            if txt_path.exists():
                with open(txt_path, 'r') as f:
                    self._words = [
                        word.strip().upper() 
                        for word in f 
                        if len(word.strip()) == 5
                    ]
                print(f"⚠️  Loaded {len(self._words)} words from legacy words.txt")
                return self._words
            raise FileNotFoundError("No wordlist found")
        
        with open(data_path, 'r') as f:
            data = json.load(f)
            self._words = [word.upper() for word in data.get("words", [])]
        
        print(f"✅ Loaded {len(self._words)} words from wordlist.json")
        return self._words
    
    @property
    def words(self) -> List[str]:
        """Get word list (loads if needed)."""
        return self.load_words()
    
    def is_valid(self, word: str) -> bool:
        """Check if word exists in dictionary."""
        return word.upper() in self.words


# Global singleton
wordlist = WordListManager()


class AgentSolver:
    """Solver that uses algorithms to suggest next guess."""
    
    def __init__(self, algorithm: str = "dfs"):
        self.algorithm = algorithm.lower()
        self.agent = create_agent(wordlist.words, self.algorithm)
    
    def solve_next(
        self, 
        guesses: List[str], 
        evaluations: List[List[str]]
    ) -> tuple[str, float, int]:
        """
        Get next best guess.
        
        Returns:
            (guess, confidence, remaining_count)
        """
        # Process previous guesses
        for i, guess in enumerate(guesses):
            if i < len(evaluations):
                self.agent.current_guesses.append(GuessResult(
                    word=guess.upper(),
                    evaluation=evaluations[i]
                ))
        
        # Filter possible words
        possible_words = self.agent.filter_possible_words(
            wordlist.words, 
            self.agent.current_guesses
        )
        
        if not possible_words:
            raise ValueError("No valid words remaining")
        
        # Get next guess
        next_guess = self.agent.choose_best_guess(possible_words)
        
        # Calculate confidence
        confidence = min(1.0 / len(possible_words), 1.0)
        
        return next_guess, confidence, len(possible_words)
    
    def get_reasoning(self, remaining_count: int, confidence: float) -> str:
        """Generate human-readable reasoning."""
        if remaining_count == 1:
            return "Only one word matches all clues!"
        elif remaining_count <= 5:
            return f"Narrowed to {remaining_count} possibilities - high confidence guess"
        elif remaining_count <= 20:
            return f"{remaining_count} words remain - strategic elimination"
        elif remaining_count <= 100:
            return f"Filtering from {remaining_count} candidates using {self.algorithm.upper()}"
        else:
            return f"Exploring {remaining_count} possibilities with {self.algorithm.upper()} algorithm"
