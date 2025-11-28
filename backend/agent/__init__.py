"""
Agent Algorithms Module

This module provides different solving algorithms for the Wordly game.
Each algorithm implements the BaseAgent interface with its own strategy.
"""

from .base_agent import BaseAgent, GuessResult
from .dfs_algorithm import DFSAgent
from .hill_climbing_algorithm import HillClimbingAgent
from .simulated_annealing_algorithm import SimulatedAnnealingAgent

__all__ = [
    'BaseAgent',
    'GuessResult',
    'DFSAgent',
    'HillClimbingAgent',
    'SimulatedAnnealingAgent',
    'create_agent',
    'get_algorithm_name',
    'get_algorithm_description'
]


def create_agent(word_list: list[str], algorithm: str) -> BaseAgent:
    """
    Factory function to create an agent based on algorithm type
    
    Args:
        word_list: List of valid words
        algorithm: Type of algorithm ('dfs', 'hill-climbing', 'simulated-annealing')
        
    Returns:
        Instance of the selected algorithm agent
    """
    algorithm = algorithm.lower()
    
    if algorithm == 'dfs':
        return DFSAgent(word_list)
    elif algorithm == 'hill-climbing':
        return HillClimbingAgent(word_list)
    elif algorithm == 'simulated-annealing':
        return SimulatedAnnealingAgent(word_list)
    else:
        print(f"Warning: Unknown algorithm '{algorithm}', defaulting to DFS")
        return DFSAgent(word_list)


def get_algorithm_name(algorithm: str) -> str:
    """Get display name for algorithm"""
    names = {
        'dfs': 'DFS (Depth-First Search)',
        'hill-climbing': 'Hill Climbing',
        'simulated-annealing': 'Simulated Annealing'
    }
    return names.get(algorithm.lower(), algorithm)


def get_algorithm_description(algorithm: str) -> str:
    """Get description for algorithm"""
    descriptions = {
        'dfs': 'Systematic exploration with frequency-based scoring. Guarantees finding a solution but may not be optimal.',
        'hill-climbing': 'Greedy local search that always chooses the best neighbor. Fast but may get stuck in local optima.',
        'simulated-annealing': 'Probabilistic algorithm that can escape local optima by accepting worse solutions with decreasing probability.'
    }
    return descriptions.get(algorithm.lower(), '')
