"""Tests for solver agents."""
import pytest
from agent import get_agent
from schema.solve_request import SolveRequest
from word_manager.word_manager import wordlist
from schema import SolverStrategy

def test_get_agent_default():
    """Test getting default agent (entropy)."""
    agent = get_agent()
    assert agent is not None
    assert hasattr(agent, "solve")

def test_get_agent_entropy():
    """Test getting entropy agent."""
    agent = get_agent(SolverStrategy.ENTROPY)
    assert agent is not None
    assert hasattr(agent, "solve")


def test_get_agent_better_entropy():
    """Test getting better_entropy agent."""
    agent = get_agent(SolverStrategy.BETTER_ENTROPY)
    assert agent is not None
    assert hasattr(agent, "solve")


def test_get_agent_frequency():
    """Test getting frequency agent."""
    agent = get_agent(SolverStrategy.FREQUENCY)
    assert agent is not None
    assert hasattr(agent, "solve")


def test_get_agent_random():
    """Test getting random agent."""
    agent = get_agent(SolverStrategy.RANDOM)
    assert agent is not None
    assert hasattr(agent, "solve")


def test_agent_first_suggestion():
    """Test that agents return valid first suggestions."""
    strategies = [SolverStrategy.ENTROPY, SolverStrategy.BETTER_ENTROPY, SolverStrategy.FREQUENCY, SolverStrategy.RANDOM]
    
    for strategy in strategies:
        agent = get_agent(strategy)
        response = agent.solve(SolveRequest(
            history=[],
        ))

        next_guess = response.next_guess
        suggestions = response.suggestions

        assert next_guess is not None
        assert len(next_guess) == 5
        assert wordlist.is_valid(next_guess)
        for suggestion in suggestions:
            assert len(suggestion) == 5
            assert wordlist.is_valid(suggestion)

        


def test_agent_with_history():
    """Test agents with guess history."""
    agent = get_agent(SolverStrategy.ENTROPY)
    
    # Simulate game history
    history = [
        {
            "guess": "AROSE",
            "feedback": "02000"  # A=0, R=2, O=0, S=0, E=0
        }
    ]
    
    response = agent.solve(SolveRequest(
        history=history,
    ))
    suggestion = response.next_guess

    assert suggestion is not None
    assert len(suggestion) == 5
    assert wordlist.is_valid(suggestion)
    # Should not contain eliminated letters
    assert "A" not in suggestion
    assert "S" not in suggestion
    assert "O" not in suggestion
    assert "E" not in suggestion
