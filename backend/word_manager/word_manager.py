"""Agent solver logic with lazy-loaded wordlist."""

import json
from pathlib import Path
from typing import List, Optional


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
        
        base_dir = Path(__file__).resolve().parent
        data_path = base_dir / "wordlist.json"
        
        if not data_path.exists():
            # Fallback to old words.txt for migration
            txt_path = base_dir / "words.txt"
            if txt_path.exists():
                with open(txt_path, 'r') as f:
                    self._words = [
                        word.strip().upper() 
                        for word in f 
                        if len(word.strip()) == 5
                    ]
                print(f"Loaded {len(self._words)} words from legacy words.txt")
                return self._words
            raise FileNotFoundError("No wordlist found")
        
        with open(data_path, 'r') as f:
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


