"""Pytest configuration and fixtures."""
import sys
from pathlib import Path

# Add backend root to Python path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_game_state():
    """Sample game state for testing."""
    return {
        "guesses": ["aleph"],
        "evaluations": ["22000"]
    }


@pytest.fixture
def sample_strategies():
    """List of available solver strategies."""
    return ["entropy", "better_entropy", "frequency", "random"]
