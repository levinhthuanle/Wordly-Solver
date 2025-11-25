from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

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
    
class GuessResponse(BaseModel):
    guess: str
    confidence: float
    remaining_words: int

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
    """
    if not word_list:
        raise HTTPException(status_code=500, detail="Word list not loaded")
    
    from agent_solver import WordlyAgentSolver
    
    try:
        # Initialize solver
        solver = WordlyAgentSolver(word_list)
        
        # Process previous guesses
        for i, guess in enumerate(request.guesses):
            if i < len(request.evaluations):
                solver.add_guess(guess.upper(), request.evaluations[i])
        
        # Get next best guess
        result = solver.get_next_guess()
        
        return GuessResponse(
            guess=result['guess'],
            confidence=result['confidence'],
            remaining_words=result['remaining_words']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver error: {str(e)}")

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
