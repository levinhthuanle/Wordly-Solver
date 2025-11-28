"""API module."""
"""API route handlers."""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from schema import (
    SolveRequest,
    SolveResponse,
    ValidateRequest,
    ValidateResponse,
    HealthResponse,
)
from agent import get_agent, SolverStrategy
from word_manager.word_manager import wordlist

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        words_count=len(wordlist.words),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.post("/api/validate", response_model=ValidateResponse)
async def validate_word(request: ValidateRequest):
    """Validate if a word exists in dictionary."""
    word_upper = request.word.strip().upper()
    is_valid = wordlist.is_valid(word_upper)
    
    return ValidateResponse(
        word=request.word,
        valid=is_valid,
        message="Valid word" if is_valid else "Word not found in dictionary"
    )


@router.post("/api/solve", response_model=SolveResponse)
async def solve_wordle(request: SolveRequest):
    """Solve Wordle based on prior guesses and feedback."""
    strategy = (
        request.parameters.strategy
        if request.parameters and request.parameters.strategy
        else SolverStrategy.ENTROPY
    )
    agent = get_agent(strategy)
    try:
        response = agent.solve(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return response

@router.get("/api/words/all")
async def get_all_words():
    """Get complete word list for frontend validation."""
    return {
        "words": wordlist.words,
        "total": len(wordlist.words),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
