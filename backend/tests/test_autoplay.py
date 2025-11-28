"""Tests for autoplay endpoint."""
import pytest


def test_autoplay_basic(client, sample_strategies):
    """Test basic autoplay functionality."""
    for strategy in sample_strategies:
        response = client.post("/api/autoplay", json={
            "strategy": strategy,
            "max_attempts": 6
        })
        assert response.status_code == 200, f"Failed for strategy: {strategy}"
        data = response.json()
        assert "answer" in data
        assert "solved" in data
        assert "steps" in data
        assert "attempts_used" in data
        assert isinstance(data["steps"], list)


def test_autoplay_with_custom_answer(client):
    """Test autoplay with specific answer."""
    response = client.post("/api/autoplay", json={
        "strategy": "entropy",
        "answer": "aleph",
        "max_attempts": 6
    })
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "ALEPH"
    assert "steps" in data
    assert len(data["steps"]) > 0


def test_autoplay_max_attempts(client):
    """Test autoplay respects max attempts limit."""
    response = client.post("/api/autoplay", json={
        "strategy": "random",
        "max_attempts": 3
    })
    assert response.status_code == 200
    data = response.json()
    assert data["attempts_used"] <= 3


def test_autoplay_step_structure(client):
    """Test that autoplay steps have correct structure."""
    response = client.post("/api/autoplay", json={
        "strategy": "entropy",
        "max_attempts": 6
    })
    assert response.status_code == 200
    data = response.json()
    
    if len(data["steps"]) > 0:
        step = data["steps"][0]
        assert "guess" in step
        assert "feedback" in step
        assert "thoughts" in step
        assert "remaining_candidates" in step
        assert len(step["guess"]) == 5
        assert len(step["feedback"]) == 5


def test_autoplay_solved_flag(client):
    """Test that solved flag is set correctly."""
    response = client.post("/api/autoplay", json={
        "strategy": "better_entropy",
        "max_attempts": 6
    })
    assert response.status_code == 200
    data = response.json()
    
    # If solved, last step should have all correct feedback
    if data["solved"]:
        last_step = data["steps"][-1]
        assert all(c == "2" for c in last_step["feedback"])
