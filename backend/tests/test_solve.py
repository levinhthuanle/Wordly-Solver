"""Tests for solve endpoint."""
import pytest


def test_solve_first_guess(client, sample_strategies):
    """Test getting first guess suggestion."""
    for strategy in sample_strategies:
        response = client.post("/api/solve", json={
            "strategy": strategy,
            "game_state": {
                "guesses": [],
                "evaluations": []
            }
        })
        assert response.status_code == 200, f"Failed for strategy: {strategy}"
        data = response.json()
        assert "next_guess" in data
        assert len(data["next_guess"]) == 5
        assert "remaining_candidates" in data
        assert data["remaining_candidates"] > 0
        assert len(data["suggestions"]) > 0


def test_solve_with_history(client, sample_game_state):
    """Test getting suggestion with guess history."""
    response = client.post("/api/solve", json={
        "strategy": "entropy",
        "game_state": sample_game_state
    })
    assert response.status_code == 200
    data = response.json()
    assert "next_guess" in data
    assert len(data["next_guess"]) == 5
    assert "remaining_candidates" in data
    assert data["remaining_candidates"] > 0
    assert len(data["suggestions"]) > 0

def test_solve_invalid_strategy(client):
    """Test solve with invalid strategy."""
    response = client.post("/api/solve", json={
        "history": {
            "guesses": [],
            "evaluations": []
        },
        "parameters": {
            "strategy": "invalid_strategy"
        }
    })
    print(response.json())
    assert response.status_code == 422  # Validation error


def test_solve_all_strategies(client, sample_strategies):
    """Test all strategies return valid suggestions."""
    for strategy in sample_strategies:
        response = client.post("/api/solve", json={
            "strategy": strategy,
            "game_state": {
                "guesses": [],
                "evaluations": []
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert data["next_guess"].isupper()
        assert data["next_guess"].isalpha()