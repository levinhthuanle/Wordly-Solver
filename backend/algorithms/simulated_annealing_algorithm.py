"""
Simulated Annealing Algorithm

Probabilistic algorithm that can escape local optima by accepting 
worse solutions with decreasing probability over time.
"""

from typing import List
import random
import math
from .base_agent import BaseAgent


class SimulatedAnnealingAgent(BaseAgent):
    """
    Simulated Annealing Algorithm Agent
    
    Strategy: Probabilistic search with temperature cooling
    - Starts from random word
    - Accepts better solutions always
    - Accepts worse solutions with probability e^(Δ/T)
    - Temperature decreases over time (cooling)
    - Can escape local optima
    """
    
    def choose_best_guess(self, possible_words: List[str]) -> str:
        """
        Choose the best guess using simulated annealing
        
        Args:
            possible_words: List of words that match all previous patterns
            
        Returns:
            The best word found by simulated annealing
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
        
        # Simulated Annealing parameters
        temperature = 100.0
        cooling_rate = 0.85
        min_temperature = 1.0
        max_iterations = 50
        
        # Start from random word
        start_index = random.randint(0, min(9, len(possible_words) - 1))
        current_word = possible_words[start_index]
        current_score = self.score_word_entropy(current_word, possible_words)
        best_word = current_word
        best_score = current_score
        
        iterations = 0
        
        while temperature > min_temperature and iterations < max_iterations:
            iterations += 1
            
            # Get random neighbor
            neighbors = self._get_neighbors(current_word, possible_words, 20)
            if not neighbors:
                break
            
            neighbor = random.choice(neighbors)
            neighbor_score = self.score_word_entropy(neighbor, possible_words)
            
            # Calculate acceptance probability
            delta = neighbor_score - current_score
            if delta > 0:
                acceptance_probability = 1.0
            else:
                acceptance_probability = math.exp(delta / temperature)
            
            # Accept or reject based on probability
            if random.random() < acceptance_probability:
                current_word = neighbor
                current_score = neighbor_score
                
                # Update best if improved
                if current_score > best_score:
                    best_word = current_word
                    best_score = current_score
            
            # Cool down temperature
            temperature *= cooling_rate
        
        return best_word
    
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
