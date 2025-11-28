"""API module."""
"""API route handlers."""

from datetime import datetime, timezone
import random
from typing import List

from fastapi import APIRouter, HTTPException

from schema import (
    AutoplayRequest,
    AutoplayResponse,
    AutoplayStep,
    GuessFeedback,
    SolveParameters,
    SolveRequest,
    SolveResponse,
    ValidateRequest,
    ValidateResponse,
    HealthResponse,
)
from agent import get_agent, SolverStrategy
from agent.base import Agent as BaseAgent
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
        word=word_upper,
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


@router.post("/api/autoplay", response_model=AutoplayResponse)
async def autoplay(request: AutoplayRequest):
    """Run a fully automated solving session for a hidden answer."""

    answer = request.answer.upper() if request.answer else random.choice(wordlist.words)
    answer = answer.strip().upper()

    if len(answer) != 5:
        raise HTTPException(status_code=400, detail="Answer must be 5 letters long.")
    if not wordlist.is_valid(answer):
        raise HTTPException(status_code=400, detail="Answer is not in the dictionary.")

    agent = get_agent(request.strategy)
    history: List[GuessFeedback] = []
    steps: List[AutoplayStep] = []
    solved = False

    for _ in range(request.max_attempts):
        parameters = SolveParameters(
            strategy=request.strategy,
            max_suggestions=1,
            allow_repeats=request.allow_repeats,
        )
        solve_request = SolveRequest(history=history, parameters=parameters)
        try:
            result = agent.solve(solve_request)
        except Exception as exc:  # pragma: no cover - agent errors bubbled up
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        guess = result.next_guess or (result.suggestions[0] if result.suggestions else None)
        if not guess:
            break

        feedback_pattern = BaseAgent._get_pattern(guess, answer)
        attempt = GuessFeedback(guess=guess, feedback=feedback_pattern)
        history.append(attempt)
        steps.append(
            AutoplayStep(
                guess=guess,
                feedback=feedback_pattern,
                thoughts=result.thoughts,
                remaining_candidates=result.remaining_candidates,
            )
        )

        if feedback_pattern == "2" * len(answer):
            solved = True
            break

    return AutoplayResponse(
        answer=answer,
        solved=solved,
        attempts_used=len(history),
        steps=steps,
    )

@router.get("/api/words/all")
async def get_all_words():
    """Get complete word list for frontend validation."""
    return {
        "words": wordlist.words,
        "total": len(wordlist.words),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
