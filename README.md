# Wordly-Solver

A Wordle-style word guessing game built with Next.js (Frontend) and FastAPI (Backend).

## Features

- 🎮 Random word selection from 14,855+ words
- 🎯 Daily challenge mode
- 🤖 AI Agent Solver with **3 algorithms**: DFS, Hill Climbing, Simulated Annealing
- 📊 Statistics tracking
- ⌨️ Keyboard support
- 🎨 Beautiful UI with animations
- 🔌 Backend API for word validation and agent solving
- 🔧 **Modular algorithm architecture** - Easy to add new solving algorithms

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

The game includes **three AI solving algorithms** that you can choose from:

### 🔍 Algorithm Comparison

| Algorithm | Strategy | Pros | Cons | Best For |
|-----------|----------|------|------|----------|
| **DFS** | Frequency-based scoring | Consistent, reliable | Can be slow | Guaranteed solutions |
| **Hill Climbing** | Greedy local search | Fast convergence | May get stuck in local optima | Quick solving |
| **Simulated Annealing** | Probabilistic search | Escapes local optima | Less predictable | Exploring solution space |

### 📁 Algorithm Architecture

All algorithms are located in `FrontEnd/src/algorithms/`:

```
algorithms/
├── base-agent.ts                    # Abstract base class (shared logic)
├── dfs-algorithm.ts                 # DFS implementation
├── hill-climbing-algorithm.ts       # Hill Climbing implementation
├── simulated-annealing-algorithm.ts # Simulated Annealing implementation
└── index.ts                         # Factory pattern & exports
```

### 🎯 Algorithm Details

#### 1. DFS (Depth-First Search)
- **Strategy**: Systematic exploration with frequency-based scoring
- **Steps**:
  1. First guess: Uses optimal starters (AROSE, SLATE, CRATE, etc.)
  2. Filter: Eliminates impossible words based on feedback patterns
  3. Score: Ranks words by letter/position frequency
  4. Choose: Selects highest-scoring word
  5. Repeat until solved

#### 2. Hill Climbing
- **Strategy**: Greedy local search - always moves to better neighbor
- **Steps**:
  1. Start: Random word from top candidates
  2. Evaluate: Score using entropy (information gain)
  3. Check neighbors: Sample 30 nearby words
  4. Move: Jump to first better neighbor found
  5. Repeat: Max 20 iterations or until no improvement

#### 3. Simulated Annealing
- **Strategy**: Probabilistic acceptance with temperature cooling
- **Steps**:
  1. Start: Random word from top candidates
  2. Temperature: Begins at 100, cools to 1 (cooling rate: 0.85)
  3. Neighbor: Pick random nearby word
  4. Accept: Always accept better, sometimes accept worse (probability = e^(Δ/T))
  5. Cool down: Reduce temperature each iteration
  6. Repeat: Max 50 iterations or until temperature drops

### 🛠️ How to Add a New Algorithm

**For Algorithm Developers:**

1. **Create your algorithm file** in `FrontEnd/src/algorithms/`:
   ```typescript
   // my-algorithm.ts
   import { BaseAgent } from "./base-agent";
   import { normalize } from "@/utils/game-utils";

   export class MyAlgorithmAgent extends BaseAgent {
     constructor(wordList: string[]) {
       super(wordList.map(w => normalize(w)));
     }

     protected chooseBestGuess(possibleWords: string[]): string {
       // Your algorithm logic here
       // Access helper methods:
       // - this.scoreWordFrequency(word, possibleWords)
       // - this.scoreWordEntropy(word, possibleWords)
       // - this.simulateEvaluation(guess, answer)
       // - this.getOptimalStarters()
       
       return bestWord;
     }
   }
   ```

2. **Add to type definitions** in `FrontEnd/src/types/types.ts`:
   ```typescript
   export type AlgorithmType = 
     | 'dfs' 
     | 'hill-climbing' 
     | 'simulated-annealing'
     | 'my-algorithm';  // Add your algorithm
   ```

3. **Register in factory** in `FrontEnd/src/algorithms/index.ts`:
   ```typescript
   import { MyAlgorithmAgent } from './my-algorithm';

   export function createAgent(wordList: string[], algorithm: AlgorithmType): BaseAgent {
     switch (algorithm) {
       case 'dfs':
         return new DFSAgent(wordList);
       case 'hill-climbing':
         return new HillClimbingAgent(wordList);
       case 'simulated-annealing':
         return new SimulatedAnnealingAgent(wordList);
       case 'my-algorithm':
         return new MyAlgorithmAgent(wordList);  // Add your case
       default:
         return new DFSAgent(wordList);
     }
   }

   export function getAlgorithmName(algorithm: AlgorithmType): string {
     // Add display name for UI
   }

   export function getAlgorithmDescription(algorithm: AlgorithmType): string {
     // Add description for UI
   }
   ```

4. **Update UI dropdown** in `FrontEnd/src/components/GameControls.tsx`:
   ```tsx
   <select value={selectedAlgorithm} onChange={...}>
     <option value="dfs">DFS (Depth-First Search)</option>
     <option value="hill-climbing">Hill Climbing</option>
     <option value="simulated-annealing">Simulated Annealing</option>
     <option value="my-algorithm">My Algorithm Name</option>
   </select>
   ```

### 📊 Available Helper Methods (from BaseAgent)

When developing your algorithm, you have access to:

```typescript
// Filter words matching all previous guess patterns
protected filterPossibleWords(words: string[], guesses: GuessResult[]): string[]

// Check if a word matches a specific guess pattern
protected wordMatchesPattern(word: string, guess: GuessResult): boolean

// Score based on letter frequency in remaining words
protected scoreWordFrequency(word: string, possibleWords: string[]): number

// Score based on entropy (information gain) - higher = better
protected scoreWordEntropy(word: string, possibleWords: string[]): number

// Simulate what feedback would be if this word was the answer
protected simulateEvaluation(guess: string, answer: string): LetterState[]

// Get optimal starting words
protected getOptimalStarters(): string[]  // Returns ['AROSE', 'SLATE', 'CRATE', 'TRACE', 'STARE']
```

### 🎮 Testing Your Algorithm

1. **Run development mode**:
   ```bash
   cd FrontEnd
   npm run dev
   ```

2. **Select your algorithm** from dropdown in the game UI

3. **Click "🤖 Agent Solve"** and watch it play

4. **Check console logs** for debugging:
   ```javascript
   console.log(`🤖 Using ${algorithm.toUpperCase()} algorithm`);
   console.log(`🤖 Agent guess (client-side): ${guess}`);
   ```

### 🔬 Algorithm Performance Metrics

To benchmark your algorithm, track these metrics:
- **Success rate**: % of games solved within 6 attempts
- **Average attempts**: Mean number of guesses to solve
- **Average time**: Execution time per guess
- **Word coverage**: % of word list it can solve

**Backend vs Client-side:**
- Backend solver (Python) is currently DFS-only
- Frontend supports all three algorithms (TypeScript)
- Automatically falls back to client-side if backend unavailable

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS, Zustand
- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Deployment**: Docker, Docker Compose
- **Algorithms**: 
  - DFS (Depth-First Search with frequency scoring)
  - Hill Climbing (Greedy local search)
  - Simulated Annealing (Probabilistic global search)
- **Architecture Pattern**: Factory pattern, Abstract base class, Modular algorithm system

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

### Adding New Algorithms (For Algorithm Researchers)

See the **"How to Add a New Algorithm"** section above for detailed instructions.

**Quick Start:**
1. Create new file in `FrontEnd/src/algorithms/`
2. Extend `BaseAgent` class
3. Implement `chooseBestGuess()` method
4. Register in factory pattern
5. Test in UI

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

### Debugging Agent Algorithms
```bash
# Frontend logs show algorithm execution
cd FrontEnd
npm run dev

# Open browser console (F12) to see:
# - Algorithm selection
# - Each guess made by agent
# - Remaining word count
# - Scoring decisions
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

