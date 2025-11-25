# Wordly-Solver

A Wordle-style word guessing game built with Next.js (Frontend) and FastAPI (Backend).

## Features

- 🎮 Random word selection from 14,855+ words
- 🎯 Daily challenge mode
- 🤖 AI Agent Solver with DFS algorithm
- 📊 Statistics tracking
- ⌨️ Keyboard support
- 🎨 Beautiful UI with animations
- 🔌 Backend API for word validation and agent solving

## Architecture

### Frontend (Next.js)
- React 19 + TypeScript
- Zustand for state management
- Tailwind CSS for styling
- Client-side game logic
- Agent solver (with backend fallback)

### Backend (FastAPI)
- Python 3.11 + FastAPI
- DFS-based agent solver
- Word validation API
- Health monitoring
- CORS enabled

## Word List

The game uses `words.txt` which contains over 14,855 five-letter words.

## How to Run

### Method 1: Docker Compose (Full Stack - Recommended)

```bash
# Make sure Docker Desktop is running
docker-compose up --build
```

**Services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Method 2: Development Mode

#### Backend:
```bash
cd Backend
pip install -r Requirements.txt
python main.py
```
Backend runs at: http://localhost:8000

#### Frontend:
```bash
cd FrontEnd
npm install
npm run dev
```
Frontend runs at: http://localhost:3000

## API Endpoints

### Backend API

```
GET  /                     - Service info
GET  /health               - Health check
POST /api/validate         - Validate word
POST /api/solve            - Get next agent guess
GET  /api/words/stats      - Word statistics
GET  /api/words/random     - Get random word
GET  /api/words/daily      - Get daily word
```

### Example API Usage

**Validate Word:**
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"word": "hello"}'
```

**Agent Solver:**
```bash
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "guesses": ["AROSE"],
    "evaluations": [["absent","absent","absent","present","absent"]]
  }'
```

## Docker Commands

```bash
# Start all services (frontend + backend)
docker-compose up -d

# View logs
docker-compose logs -f

# View backend logs only
docker-compose logs -f backend

# View frontend logs only
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build

# Remove everything (including volumes)
docker-compose down -v
```

## Game Rules

1. Guess the 5-letter word in 6 attempts
2. 🟩 Green = Correct letter in correct position
3. 🟨 Yellow = Correct letter in wrong position
4. ⬛ Gray = Letter not in word
5. 🤖 Agent = Let AI solve it for you!

## Agent Solver

The agent uses a **DFS (Depth-First Search)** algorithm with smart pruning:

1. **First guess:** Uses optimal starter words (AROSE, SLATE, etc.)
2. **Filter:** Eliminates impossible words based on feedback
3. **Score:** Ranks remaining words by information gain
4. **Choose:** Selects word that maximizes letter/position frequency
5. **Repeat:** Until word is found or max attempts reached

**Backend vs Client-side:**
- Backend solver runs on Python (faster for large word lists)
- Automatically falls back to client-side if backend unavailable

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS, Zustand
- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Deployment**: Docker, Docker Compose
- **Algorithm**: DFS with pattern matching and frequency analysis

## Environment Variables

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

### Backend
```env
PYTHONUNBUFFERED=1
```

## Development

### Backend Development
```bash
cd Backend
pip install -r Requirements.txt

# Run with auto-reload
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd FrontEnd
npm install
npm run dev
```

## Testing

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Get word stats
curl http://localhost:8000/api/words/stats

# Validate word
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"word": "tests"}'
```

## Troubleshooting

### Backend not connecting
1. Check Docker logs: `docker-compose logs backend`
2. Verify backend health: `curl http://localhost:8000/health`
3. Check CORS settings in `main.py`

### Frontend can't reach backend
1. Check `NEXT_PUBLIC_API_URL` environment variable
2. Verify both services are running: `docker-compose ps`
3. Check browser console for CORS errors

### Port conflicts
```bash
# Check what's using port 3000
netstat -ano | findstr :3000

# Check what's using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F
```

## License

MIT

