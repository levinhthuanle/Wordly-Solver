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
