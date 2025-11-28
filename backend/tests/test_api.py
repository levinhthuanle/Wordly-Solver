"""Tests for API endpoints."""
import pytest


def test_root_endpoint(client):
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Wordly Solver API"
    assert "version" in data
    assert "endpoints" in data


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "words_count" in data
    assert data["words_count"] > 0
    assert "timestamp" in data


def test_validate_valid_word(client):
    """Test validation endpoint with valid word."""
    response = client.post("/api/validate", json={"word": "aleph"})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["word"] == "ALEPH"


def test_validate_invalid_word(client):
    """Test validation endpoint with invalid word."""
    response = client.post("/api/validate", json={"word": "ZZZZZ"})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False


def test_validate_case_insensitive(client):
    """Test validation is case-insensitive."""
    response = client.post("/api/validate", json={"word": "aleph"})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True


def test_get_all_words(client):
    """Test getting all words endpoint."""
    response = client.get("/api/words/all")
    assert response.status_code == 200
    words = response.json()
    assert isinstance(words, dict)
    assert len(words["words"]) > 1000
    assert all(isinstance(w, str) for w in words["words"])
    assert all(len(w) == 5 for w in words["words"][:100])
