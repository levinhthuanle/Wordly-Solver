from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

# Import history module
from history import game_history

app = FastAPI(title="Wordly Solver API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load word list
word_list = []

def load_words():
    global word_list
    try:
        with open('words.txt', 'r') as f:
            word_list = [word.strip().upper() for word in f.readlines() if len(word.strip()) == 5]
        print(f"✅ Loaded {len(word_list)} words")
    except FileNotFoundError:
        print("⚠️ words.txt not found, using empty word list")
        word_list = []

# Load words on startup
@app.on_event("startup")
async def startup_event():
    load_words()

# Models
class ValidateRequest(BaseModel):
    word: str

class SolveRequest(BaseModel):
    guesses: List[str]
    evaluations: List[List[str]]
    algorithm: Optional[str] = "dfs"  # Default to DFS

class AgentRunRequest(BaseModel):
    """Request to run agent from start to finish"""
    answer: str
    algorithm: Optional[str] = "dfs"
    max_attempts: Optional[int] = 6
    
class GuessResponse(BaseModel):
    guess: str
    confidence: float
    remaining_words: int
    algorithm: str

class AgentRunResponse(BaseModel):
    """Response from agent run"""
    success: bool
    attempts: int
    guesses: List[str]
    evaluations: List[List[str]]
    algorithm: str
    message: str

class GameHistoryRequest(BaseModel):
    """Request to save game history"""
    word: str
    won: bool
    attempts: int
    score: int
    guesses: List[str]
    evaluations: List[List[str]]
    user_id: Optional[str] = None

class GameHistoryResponse(BaseModel):
    """Response with game history record"""
    id: int
    word: str
    won: bool
    attempts: int
    score: int
    guesses: List[str]
    evaluations: List[List[str]]
    date: str
    user_id: Optional[str] = None

# Health check
@app.get("/")
async def root():
    return {
        "service": "Wordly Solver API",
        "status": "running",
        "words_loaded": len(word_list),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "words_count": len(word_list)
    }

# Validate word endpoint
@app.post("/api/validate")
async def validate_word(request: ValidateRequest):
    word_upper = request.word.strip().upper()
    is_valid = word_upper in word_list
    
    return {
        "word": request.word,
        "valid": is_valid,
        "message": "Valid word" if is_valid else "Word not found in dictionary"
    }

# Get word list stats
@app.get("/api/words/stats")
async def get_word_stats():
    if not word_list:
        return {"error": "Word list not loaded"}
    
    # Letter frequency analysis
    letter_freq = {}
    for word in word_list:
        for letter in word:
            letter_freq[letter] = letter_freq.get(letter, 0) + 1
    
    return {
        "total_words": len(word_list),
        "letter_frequency": dict(sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)[:10]),
        "sample_words": word_list[:10]
    }

# Agent Solver endpoint
@app.post("/api/solve", response_model=GuessResponse)
async def solve_next_guess(request: SolveRequest):
    """
    Agent solver that returns next best guess based on previous attempts
    Supports multiple algorithms: dfs, hill-climbing, simulated-annealing
    """
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    from algorithms import create_agent
    
    try:
        # Normalize algorithm name
        algorithm = request.algorithm.lower() if request.algorithm else "dfs"
        
        # Create agent with selected algorithm
        agent = create_agent(word_list, algorithm)
        
        # Process previous guesses
        for i, guess in enumerate(request.guesses):
            if i < len(request.evaluations):
                from algorithms.base_agent import GuessResult
                agent.current_guesses.append(GuessResult(
                    word=guess.upper(),
                    evaluation=request.evaluations[i]
                ))
        
        # Filter possible words based on previous guesses
        possible_words = agent.filter_possible_words(word_list, agent.current_guesses)
        
        if not possible_words:
            raise HTTPException(status_code=400, detail="No valid words remaining")
        
        # Get next best guess
        next_guess = agent.choose_best_guess(possible_words)
        
        # Calculate confidence based on remaining words
        confidence = 1.0 / len(possible_words) if len(possible_words) > 0 else 1.0
        confidence = min(confidence, 1.0)
        
        return GuessResponse(
            guess=next_guess,
            confidence=confidence,
            remaining_words=len(possible_words),
            algorithm=algorithm
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}")

# Run full agent game endpoint
@app.post("/api/agent/run", response_model=AgentRunResponse)
async def run_agent_game(request: AgentRunRequest):
    """
    Run agent solver from start to finish
    Agent plays the full game autonomously
    """
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    from algorithms import create_agent
    
    try:
        algorithm = request.algorithm.lower() if request.algorithm else "dfs"
        max_attempts = request.max_attempts or 6
        answer = request.answer.upper()
        
        # Validate answer exists in word list
        if answer not in word_list:
            raise HTTPException(status_code=400, detail=f"Answer '{answer}' not in word list")
        
        # Create agent
        agent = create_agent(word_list, algorithm)
        
        guesses = []
        evaluations = []
        attempts = 0
        solved = False
        
        # Run agent until solved or max attempts reached
        while attempts < max_attempts and not solved:
            # Get next guess from agent
            guess = agent.solve_step(answer)
            
            if not guess:
                break
            
            guesses.append(guess)
            
            # Get evaluation from last guess
            if agent.current_guesses:
                last_evaluation = agent.current_guesses[-1].evaluation
                evaluations.append(last_evaluation)
                
                # Check if solved (all correct)
                if all(state == 'correct' for state in last_evaluation):
                    solved = True
            
            attempts += 1
        
        message = f"Solved in {attempts} attempts!" if solved else f"Failed to solve in {max_attempts} attempts"
        
        return AgentRunResponse(
            success=solved,
            attempts=attempts,
            guesses=guesses,
            evaluations=evaluations,
            algorithm=algorithm,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent run error: {str(e)}")

# ==================== HISTORY ENDPOINTS ====================

@app.post("/api/history", response_model=GameHistoryResponse)
async def save_game_history(request: GameHistoryRequest):
    """
    Save a game to history
    """
    try:
        record = game_history.add_game(
            word=request.word,
            won=request.won,
            attempts=request.attempts,
            score=request.score,
            guesses=request.guesses,
            evaluations=request.evaluations,
            user_id=request.user_id
        )
        return GameHistoryResponse(**record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save history: {str(e)}")

@app.get("/api/history")
async def get_game_history(user_id: Optional[str] = None, limit: Optional[int] = None):
    """
    Get game history
    
    Query parameters:
    - user_id: Filter by user (optional)
    - limit: Maximum number of records (optional)
    """
    try:
        games = game_history.get_all_games(user_id=user_id, limit=limit)
        return {
            "total": len(games),
            "games": games
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@app.get("/api/history/stats")
async def get_history_statistics(user_id: Optional[str] = None):
    """
    Get aggregated game statistics
    
    Query parameters:
    - user_id: Filter by user (optional)
    """
    try:
        stats = game_history.get_statistics(user_id=user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@app.delete("/api/history")
async def clear_game_history(user_id: Optional[str] = None):
    """
    Clear game history
    
    Query parameters:
    - user_id: Only clear this user's history (optional)
    """
    try:
        game_history.clear_history(user_id=user_id)
        return {
            "success": True,
            "message": f"History cleared{' for user ' + user_id if user_id else ''}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")

# Get random word
@app.get("/api/words/random")
async def get_random_word():
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    import random
    word = random.choice(word_list)
    
    return {
        "word": word,
        "length": len(word),
        "timestamp": datetime.utcnow().isoformat()
    }

# Get all words
@app.get("/api/words/all")
async def get_all_words():
    """
    Get complete word list for frontend validation
    """
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    return {
        "words": word_list,
        "total": len(word_list),
        "timestamp": datetime.utcnow().isoformat()
    }

# Get daily word (deterministic based on date)
@app.get("/api/words/daily")
async def get_daily_word():
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    from datetime import date
    
    # Deterministic seed based on date
    today = date.today()
    epoch = date(2021, 6, 19)  # Wordle epoch
    day_number = (today - epoch).days
    
    index = day_number % len(word_list)
    word = word_list[index]
    
    return {
        "word": word,
        "date": today.isoformat(),
        "day_number": day_number,
        "index": index
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
