from typing import List, Dict, Set

class WordlyAgentSolver:
    """
    DFS-based solver for Wordly game
    """
    
    def __init__(self, word_list: List[str]):
        self.all_words = [w.upper() for w in word_list]
        self.possible_words = self.all_words.copy()
        self.guesses: List[Dict] = []
        
    def add_guess(self, guess: str, evaluation: List[str]):
        """Add a guess and its evaluation to filter possible words"""
        self.guesses.append({
            'word': guess.upper(),
            'evaluation': evaluation
        })
        self._filter_words()
        
    def _filter_words(self):
        """Filter possible words based on all guesses"""
        filtered = []
        
        for word in self.possible_words:
            if self._matches_all_patterns(word):
                filtered.append(word)
        
        self.possible_words = filtered
        
    def _matches_all_patterns(self, word: str) -> bool:
        """Check if word matches all guess patterns"""
        for guess_data in self.guesses:
            if not self._matches_pattern(word, guess_data['word'], guess_data['evaluation']):
                return False
        return True
    
    def _matches_pattern(self, word: str, guess: str, evaluation: List[str]) -> bool:
        """Check if word matches a single guess pattern"""
        word_letters = list(word)
        guess_letters = list(guess)
        
        # Check correct positions (green)
        for i in range(5):
            if evaluation[i] == 'correct':
                if word_letters[i] != guess_letters[i]:
                    return False
        
        # Check present letters (yellow)
        for i in range(5):
            letter = guess_letters[i]
            
            if evaluation[i] == 'present':
                # Letter must be in word but not at this position
                if word_letters[i] == letter:
                    return False
                if letter not in word_letters:
                    return False
                    
            elif evaluation[i] == 'absent':
                # Letter should not be in word (unless correct/present elsewhere)
                has_correct_or_present = any(
                    guess_letters[j] == letter and evaluation[j] in ['correct', 'present']
                    for j in range(5)
                )
                if not has_correct_or_present and letter in word_letters:
                    return False
        
        return True
    
    def get_next_guess(self) -> Dict:
        """Get the next best guess using DFS strategy"""
        if len(self.possible_words) == 0:
            return {
                'guess': '',
                'confidence': 0.0,
                'remaining_words': 0
            }
        
        if len(self.possible_words) == 1:
            return {
                'guess': self.possible_words[0],
                'confidence': 1.0,
                'remaining_words': 1
            }
        
        # First guess: use optimal starter words
        if len(self.guesses) == 0:
            starters = ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE']
            for starter in starters:
                if starter in self.possible_words:
                    return {
                        'guess': starter,
                        'confidence': 0.8,
                        'remaining_words': len(self.possible_words)
                    }
        
        # Score and choose best word
        best_word = self._choose_best_word()
        confidence = 1.0 / len(self.possible_words) if len(self.possible_words) > 0 else 0.0
        
        return {
            'guess': best_word,
            'confidence': min(confidence * 5, 1.0),  # Scale confidence
            'remaining_words': len(self.possible_words)
        }
    
    def _choose_best_word(self) -> str:
        """Choose word that provides most information"""
        if len(self.possible_words) <= 1:
            return self.possible_words[0] if self.possible_words else ''
        
        # Calculate letter frequencies
        letter_freq: Dict[str, int] = {}
        position_freq: Dict[str, int] = {}
        
        for word in self.possible_words:
            for i, letter in enumerate(word):
                letter_freq[letter] = letter_freq.get(letter, 0) + 1
                key = f"{i}-{letter}"
                position_freq[key] = position_freq.get(key, 0) + 1
        
        # Score each word
        best_score = -1
        best_word = self.possible_words[0]
        
        # Only score first 100 words for performance
        sample_size = min(100, len(self.possible_words))
        
        for word in self.possible_words[:sample_size]:
            score = self._score_word(word, letter_freq, position_freq)
            if score > best_score:
                best_score = score
                best_word = word
        
        return best_word
    
    def _score_word(self, word: str, letter_freq: Dict[str, int], position_freq: Dict[str, int]) -> float:
        """Score a word based on information gain"""
        score = 0.0
        seen_letters: Set[str] = set()
        
        for i, letter in enumerate(word):
            # Letter frequency score
            if letter not in seen_letters:
                score += letter_freq.get(letter, 0)
                seen_letters.add(letter)
            
            # Position frequency score (weighted higher)
            key = f"{i}-{letter}"
            score += position_freq.get(key, 0) * 2
        
        return score
    
    def reset(self):
        """Reset solver state"""
        self.possible_words = self.all_words.copy()
        self.guesses = []
