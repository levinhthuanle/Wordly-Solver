"""API route handlers."""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from backend.schema import (
    SolveRequest,
    SolveResponse,
    ValidateRequest,
    ValidateResponse,
    HealthResponse,
)
from backend.agent import AgentSolver, wordlist


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
async def solve_next_guess(request: SolveRequest):
    """
    Get AI suggestion for next guess.
    Compatible with frontend AISuggestion flow.
    """
    try:
        solver = AgentSolver(algorithm=request.algorithm)
        
        guess, confidence, remaining = solver.solve_next(
            request.guesses,
            request.evaluations
        )
        
        reasoning = solver.get_reasoning(remaining, confidence)
        
        return SolveResponse(
            word=guess,
            confidence=confidence,
            reasoning=reasoning,
            remaining_count=remaining,
            algorithm=request.algorithm
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}")


@router.get("/api/words/all")
async def get_all_words():
    """Get complete word list for frontend validation."""
    return {
        "words": wordlist.words,
        "total": len(wordlist.words),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
