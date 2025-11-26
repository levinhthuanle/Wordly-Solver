# Wordly Solver Backend

Modern FastAPI backend for the Wordly puzzle solver.

## Quick Start

```bash
# Install dependencies with uv
uv pip install -e .

# Or with pip
pip install -e .

# Run development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/solve` - Get next word suggestion
- `POST /api/validate` - Validate a word
- `GET /api/words/all` - Get all valid words
- `GET /health` - Health check

See main project README for detailed API documentation.
