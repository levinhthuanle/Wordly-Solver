"""
DFS (Depth-First Search) Algorithm

Systematic exploration with frequency-based scoring.
This algorithm uses letter and position frequency to choose the best guess.
"""

from typing import List
from .base_agent import BaseAgent


class DFSAgent(BaseAgent):
    """
    DFS Algorithm Agent
    
    Strategy: Systematic exploration with frequency-based scoring
    - Uses optimal starting words
    - Scores words based on letter frequency in remaining possibilities
    - Chooses word with highest frequency score
    """
    
    def choose_best_guess(self, possible_words: List[str]) -> str:
        """
        Choose the best guess using frequency-based scoring
        
        Args:
            possible_words: List of words that match all previous patterns
            
        Returns:
            The word with the highest frequency score
        """
        # If only one word left, return it
        if len(possible_words) == 1:
            return possible_words[0]
        
        # First guess: use optimal starter
        if len(self.current_guesses) == 0:
            starters = self.get_optimal_starters()
            for starter in starters:
                if starter in possible_words:
                    return starter
        
        # Find word with highest frequency score
        best_word = possible_words[0]
        best_score = -1.0
        
        # Limit search to avoid performance issues
        search_space = possible_words[:min(100, len(possible_words))]
        
        for word in search_space:
            score = self.score_word_frequency(word, possible_words)
            if score > best_score:
                best_score = score
                best_word = word
        
        return best_word
