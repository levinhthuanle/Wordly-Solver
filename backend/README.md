# Wordly Solver - backend

A simple FastAPI-based backend for AI-powered Wordle solving with multiple strategic algorithms.

## Project Structure

```
backend/
├── agent/                  # Solver algorithms
│   ├── __init__.py         # Factory for creating the agent. 
│   ├── base.py             # Base agent interface
│   ├── entropy.py          # Information theory-based solver
│   ├── better_entropy.py   # Information theory-based solver
│   ├── frequency.py        # Letter frequency solver
│   └── random.py           # Random guess solver
├── api/                    # API routes
│   └── __init__.py         # Endpoint definitions
├── schema/                 # Data models
│   ├── game_state.py       # Game state types
│   ├── solve_request.py    # Request schemas
│   ├── solve_response.py   # Response schemas
│   └── validate.py         # Validation schemas
├── word_manager/           # Word list management
│   ├── word_manager.py     # Word loading and filtering
│   └── wordlist.json       # 10,000+ valid words
├── main.py                 # FastAPI application entry point
├── pyproject.toml          # Project dependencies and config
└── Dockerfile              # Production container definition
```

## API Endpoints

### Core Endpoints

- **`GET /`** - API information and available endpoints
- **`GET /health`** - Health check for monitoring

### Solver Endpoints

- **`POST /api/solve`** - Get next word suggestion based on game state
  - Strategies: `entropy`, `better_entropy`, `frequency`, `random`
  - Supports guess history and feedback patterns
  
- **`POST /api/autoplay`** - Run complete automated game simulation
  - Returns full transcript with reasoning for each step
  - Configurable max attempts and answer

### Word Management

- **`POST /api/validate`** - Validate if a word is in the word list
- **`GET /api/words/all`** - Retrieve complete word list (10,000+ words)

## Development

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

```bash
# Install dependencies
uv sync

# Install dependencies (for develop and test)
uv sync --all-extras

# Run development server with hot reload
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or activate venv and run directly
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Available Strategies

1. **Random** - Random valid word selection
2. **Frequency** - Letter frequency-based guessing
3. **Entropy** - Classic information theory approach, performed on the candidate set
4. **K-beam** - Entropy for the k best answers based on the frequency
5. **Better Entropy** - Entropy with the same heuristic, but performed on the total dictionary


## Docker
(AI-generated. Check carefully)

### Build and Run

```bash
# Build the image
docker build -t wordly-solver-backend .

# Run the container
docker run -p 8000:8000 wordly-solver-backend
```

### Docker Compose (Recommended)

```bash
# From project root with both frontend and backend
docker-compose up --build
```

The Dockerfile uses:
- Multi-stage builds for minimal image size
- `uv` for fast dependency resolution
- Health checks for container orchestration
- Non-root user for security

## Testing
```bash
# Run tests with pytest
uv run pytest

# Run the performance test only (recommended since this takes a lot of time)
uv run pytest tests -v -s tests/test_performance.py

# Run the other tests
uv run pytest tests -v -s --ignore=tests/test_performance.py

# Run with coverage
uv run pytest --cov=. --cov-report=html
```
