"""
Game History Storage Module

This module handles storage and retrieval of game history/scores.
Separated from agent logic to maintain clean architecture.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class GameHistoryStorage:
    """Manages game history storage in JSON file"""
    
    def __init__(self, storage_path: str = "storage/game_history.json"):
        """
        Initialize history storage
        
        Args:
            storage_path: Path to JSON file for storing history
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage directory and file if they don't exist"""
        # Create directory
        storage_dir = os.path.dirname(self.storage_path)
        if storage_dir and not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        # Create empty file if doesn't exist
        if not os.path.exists(self.storage_path):
            self._save_data([])
    
    def _load_data(self) -> List[Dict]:
        """Load all history data from file"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """Save history data to file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_game(
        self,
        word: str,
        won: bool,
        attempts: int,
        score: int,
        guesses: List[str],
        evaluations: List[List[str]],
        user_id: Optional[str] = None
    ) -> Dict:
        """
        Add a game to history
        
        Args:
            word: The target word
            won: Whether the game was won
            attempts: Number of attempts used
            score: Final score
            guesses: List of guessed words
            evaluations: List of evaluation results
            user_id: Optional user identifier
            
        Returns:
            The created game record
        """
        data = self._load_data()
        
        game_record = {
            "id": len(data) + 1,
            "word": word.upper(),
            "won": won,
            "attempts": attempts,
            "score": score,
            "guesses": guesses,
            "evaluations": evaluations,
            "date": datetime.utcnow().isoformat(),
            "user_id": user_id
        }
        
        data.append(game_record)
        self._save_data(data)
        
        return game_record
    
    def get_all_games(
        self,
        user_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get all games, optionally filtered by user
        
        Args:
            user_id: Optional user filter
            limit: Maximum number of games to return
            
        Returns:
            List of game records
        """
        data = self._load_data()
        
        # Filter by user if specified
        if user_id:
            data = [g for g in data if g.get("user_id") == user_id]
        
        # Sort by date (newest first)
        data.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # Apply limit
        if limit:
            data = data[:limit]
        
        return data
    
    def get_statistics(self, user_id: Optional[str] = None) -> Dict:
        """
        Get aggregated statistics
        
        Args:
            user_id: Optional user filter
            
        Returns:
            Dictionary with statistics
        """
        games = self.get_all_games(user_id=user_id)
        
        if not games:
            return {
                "total_games": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "average_attempts": 0.0,
                "average_score": 0.0,
                "guess_distribution": {str(i): 0 for i in range(1, 7)},
                "current_streak": 0,
                "max_streak": 0
            }
        
        total_games = len(games)
        wins = sum(1 for g in games if g["won"])
        losses = total_games - wins
        
        # Calculate average attempts (only for won games)
        won_games = [g for g in games if g["won"]]
        avg_attempts = (
            sum(g["attempts"] for g in won_games) / len(won_games)
            if won_games else 0.0
        )
        
        # Calculate average score
        avg_score = sum(g["score"] for g in games) / total_games
        
        # Guess distribution (only for won games)
        guess_dist = {str(i): 0 for i in range(1, 7)}
        for game in won_games:
            attempts = game["attempts"]
            if 1 <= attempts <= 6:
                guess_dist[str(attempts)] += 1
        
        # Calculate streaks
        current_streak = 0
        max_streak = 0
        temp_streak = 0
        
        # Reverse to calculate from oldest to newest
        for game in reversed(games):
            if game["won"]:
                temp_streak += 1
                max_streak = max(max_streak, temp_streak)
            else:
                temp_streak = 0
        
        # Current streak (from newest games)
        for game in games:
            if game["won"]:
                current_streak += 1
            else:
                break
        
        return {
            "total_games": total_games,
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / total_games * 100, 2),
            "average_attempts": round(avg_attempts, 2),
            "average_score": round(avg_score, 2),
            "guess_distribution": guess_dist,
            "current_streak": current_streak,
            "max_streak": max_streak
        }
    
    def clear_history(self, user_id: Optional[str] = None):
        """
        Clear history, optionally for specific user
        
        Args:
            user_id: If provided, only clear this user's history
        """
        if user_id:
            data = self._load_data()
            data = [g for g in data if g.get("user_id") != user_id]
            self._save_data(data)
        else:
            self._save_data([])


# Global instance
game_history = GameHistoryStorage()
