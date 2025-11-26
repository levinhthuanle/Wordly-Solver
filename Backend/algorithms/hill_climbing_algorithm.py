"""
Hill Climbing Algorithm

Greedy local search that always chooses the best neighbor.
Fast convergence but may get stuck in local optima.
"""

from typing import List
import random
from .base_agent import BaseAgent


class HillClimbingAgent(BaseAgent):
    """
    Hill Climbing Algorithm Agent
    
    Strategy: Greedy local search - always moves to better neighbor
    - Starts from random word
    - Iteratively improves by choosing best neighbor
    - Stops when no better neighbor is found (local optimum)
    """
    
    def choose_best_guess(self, possible_words: List[str]) -> str:
        """
        Choose the best guess using hill climbing
        
        Args:
            possible_words: List of words that match all previous patterns
            
        Returns:
            The word found by hill climbing
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
        
        # Hill Climbing: Start from random word, iteratively improve
        start_index = random.randint(0, min(9, len(possible_words) - 1))
        current_word = possible_words[start_index]
        current_score = self.score_word_entropy(current_word, possible_words)
        improved = True
        
        max_iterations = 20
        iterations = 0
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            # Check neighbors (random sample from possible words)
            sample_size = min(30, len(possible_words))
            neighbors = self._get_neighbors(current_word, possible_words, sample_size)
            
            for neighbor in neighbors:
                neighbor_score = self.score_word_entropy(neighbor, possible_words)
                if neighbor_score > current_score:
                    current_word = neighbor
                    current_score = neighbor_score
                    improved = True
                    break  # Take first improvement (greedy)
        
        return current_word
    
    def _get_neighbors(self, word: str, possible_words: List[str], sample_size: int) -> List[str]:
        """
        Get neighbors of a word (random sample from possible words)
        
        Args:
            word: Current word
            possible_words: List of all possible words
            sample_size: Number of neighbors to sample
            
        Returns:
            List of neighbor words
        """
        neighbors = []
        
        # Random sample from possible words
        shuffled = possible_words.copy()
        random.shuffle(shuffled)
        neighbors.extend(shuffled[:sample_size])
        
        # Remove duplicates and the current word
        neighbors = list(set(neighbors))
        if word in neighbors:
            neighbors.remove(word)
        
        return neighbors
