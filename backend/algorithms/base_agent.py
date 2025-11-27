"""
Base Agent Abstract Class

This module provides the abstract base class for all Wordly solving algorithms.
All algorithms must inherit from BaseAgent and implement the chooseBestGuess method.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from dataclasses import dataclass
import math
import random


@dataclass
class GuessResult:
    """Represents a guess and its evaluation"""
    word: str
    evaluation: List[str]  # 'correct', 'present', 'absent'


class BaseAgent(ABC):
    """Abstract base class for all Wordly solving algorithms"""
    
    def __init__(self, word_list: List[str]):
        """
        Initialize the agent with a word list
        
        Args:
            word_list: List of valid 5-letter words (normalized to uppercase)
        """
        self.word_list = [word.upper() for word in word_list]
        self.current_guesses: List[GuessResult] = []
    
    def solve_step(self, answer: str) -> str:
        """
        Main method to get the next guess
        
        Args:
            answer: The target word (for evaluation)
            
        Returns:
            The next guess, or None if no valid words remain
        """
        possible_words = self.filter_possible_words(self.word_list, self.current_guesses)
        
        if not possible_words:
            return None
        
        next_guess = self.choose_best_guess(possible_words)
        evaluation = self.evaluate_guess(answer, next_guess)
        
        self.current_guesses.append(GuessResult(
            word=next_guess,
            evaluation=evaluation
        ))
        
        return next_guess
    
    @abstractmethod
    def choose_best_guess(self, possible_words: List[str]) -> str:
        """
        Abstract method that each algorithm must implement
        
        Args:
            possible_words: List of words that match all previous patterns
            
        Returns:
            The best word to guess next
        """
        pass
    
    def filter_possible_words(self, words: List[str], guesses: List[GuessResult]) -> List[str]:
        """
        Filter words that match all previous guess patterns
        
        Args:
            words: List of all valid words
            guesses: List of previous guesses with their evaluations
            
        Returns:
            List of words that could still be the answer
        """
        return [word for word in words if all(
            self.word_matches_pattern(word, guess) for guess in guesses
        )]
    
    def word_matches_pattern(self, word: str, guess: GuessResult) -> bool:
        """
        Check if a word matches a guess pattern
        
        Args:
            word: The word to check
            guess: Previous guess with evaluation
            
        Returns:
            True if word matches the pattern, False otherwise
        """
        guess_word = guess.word
        evaluation = guess.evaluation
        word_letters = list(word)
        guess_letters = list(guess_word)
        
        # Check correct positions
        for i in range(len(guess_letters)):
            if evaluation[i] == 'correct':
                if word_letters[i] != guess_letters[i]:
                    return False
        
        # Check present and absent
        for i in range(len(guess_letters)):
            letter = guess_letters[i]
            
            if evaluation[i] == 'present':
                # Letter must be in word but not at this position
                if word_letters[i] == letter:
                    return False
                if letter not in word_letters:
                    return False
            elif evaluation[i] == 'absent':
                # Check if this letter has 'correct' or 'present' elsewhere
                letter_has_correct_or_present = any(
                    guess_letters[idx] == letter and evaluation[idx] in ['correct', 'present']
                    for idx in range(len(evaluation))
                )
                
                # If letter is marked absent and doesn't appear as correct/present elsewhere,
                # it shouldn't be in the word
                if not letter_has_correct_or_present and letter in word_letters:
                    return False
        
        return True
    
    def evaluate_guess(self, answer: str, guess: str) -> List[str]:
        """
        Evaluate a guess against the answer
        
        Args:
            answer: The target word
            guess: The guessed word
            
        Returns:
            List of evaluation results ('correct', 'present', 'absent')
        """
        result = ['absent'] * 5
        answer_letters = list(answer.upper())
        guess_letters = list(guess.upper())
        used = [False] * 5
        
        # Mark correct positions
        for i in range(5):
            if guess_letters[i] == answer_letters[i]:
                result[i] = 'correct'
                used[i] = True
        
        # Mark present positions
        for i in range(5):
            if result[i] == 'correct':
                continue
            
            for j in range(5):
                if not used[j] and guess_letters[i] == answer_letters[j]:
                    result[i] = 'present'
                    used[j] = True
                    break
        
        return result
    
    def score_word_frequency(self, word: str, possible_words: List[str]) -> float:
        """
        Score word based on letter frequency in remaining possible words
        
        Args:
            word: Word to score
            possible_words: List of remaining possible words
            
        Returns:
            Frequency score (higher is better)
        """
        score = 0.0
        letters = list(word)
        
        # Count letter frequencies
        letter_freq: Dict[str, int] = {}
        position_freq: Dict[str, int] = {}
        
        for possible_word in possible_words:
            for i, letter in enumerate(possible_word):
                letter_freq[letter] = letter_freq.get(letter, 0) + 1
                key = f"{i}-{letter}"
                position_freq[key] = position_freq.get(key, 0) + 1
        
        # Score based on unique letters
        unique_letters = set(letters)
        for letter in unique_letters:
            score += letter_freq.get(letter, 0)
        
        # Bonus for position frequency
        for i, letter in enumerate(letters):
            key = f"{i}-{letter}"
            score += position_freq.get(key, 0) * 2
        
        return score
    
    def score_word_entropy(self, word: str, possible_words: List[str]) -> float:
        """
        Score word based on entropy (information gain)
        
        Args:
            word: Word to score
            possible_words: List of remaining possible words
            
        Returns:
            Entropy score (higher is better)
        """
        if len(possible_words) <= 1:
            return 0.0
        
        # Calculate pattern distribution
        patterns: Dict[str, int] = {}
        
        # Limit to avoid performance issues
        sample_size = min(200, len(possible_words))
        sample_words = possible_words[:sample_size]
        
        for candidate in sample_words:
            evaluation = self.evaluate_guess(candidate, word)
            pattern_key = ','.join(evaluation)
            patterns[pattern_key] = patterns.get(pattern_key, 0) + 1
        
        # Calculate entropy: -Σ(p * log2(p))
        entropy = 0.0
        total = len(sample_words)
        
        for count in patterns.values():
            if count > 0:
                probability = count / total
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def get_optimal_starters(self) -> List[str]:
        """
        Get optimal starting words
        
        Returns:
            List of good starting words
        """
        return ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE']
    
    def reset(self):
        """Reset agent state for new game"""
        self.current_guesses = []
    
    def get_guess_history(self) -> List[GuessResult]:
        """Get guess history"""
        return self.current_guesses.copy()
