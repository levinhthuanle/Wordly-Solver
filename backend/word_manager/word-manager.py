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


