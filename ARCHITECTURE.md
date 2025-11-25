# Architecture Overview - Wordly Solver

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client                              │
│                    (Browser/React)                          │
├─────────────────────────────────────────────────────────────┤
│  • Game UI (Next.js)                                        │
│  • State Management (Zustand)                               │
│  • Client-side Agent Solver (Fallback)                      │
│  • LocalStorage (Stats/Scores)                              │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Server                          │
│                      (Next.js 16)                           │
├─────────────────────────────────────────────────────────────┤
│  • SSR/SSG                                                  │
│  • API Routes (/api/stats)                                  │
│  • Static Assets (words.txt)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    Backend Server                           │
│                   (FastAPI/Python)                          │
├─────────────────────────────────────────────────────────────┤
│  • DFS Agent Solver API                                     │
│  • Word Validation Service                                  │
│  • Daily/Random Word Generator                              │
│  • Letter Frequency Analysis                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
Wordly-Solver/
├── Backend/                    # Python FastAPI Server
│   ├── main.py                # FastAPI app & endpoints
│   ├── agent_solver.py        # DFS solver algorithm
│   ├── words.txt              # 14,855 words
│   ├── Requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container config
│
├── FrontEnd/                  # Next.js Application
│   ├── public/
│   │   └── words.txt          # Static word list
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   │   ├── page.tsx       # Home page
│   │   │   ├── layout.tsx     # Root layout
│   │   │   └── api/           # API routes
│   │   │       └── stats/     # Stats endpoint
│   │   ├── components/        # React components
│   │   │   ├── WordlyMain.tsx
│   │   │   ├── GameBoard.tsx
│   │   │   ├── GameControls.tsx
│   │   │   └── ...
│   │   ├── hooks/             # React hooks
│   │   │   ├── useGameController.ts
│   │   │   ├── useAgentSolver.ts
│   │   │   └── useGameStats.ts
│   │   ├── stores/            # Zustand stores
│   │   │   └── game-store.ts
│   │   ├── utils/             # Utilities
│   │   │   ├── game-utils.ts
│   │   │   ├── agent-solver.ts
│   │   │   ├── word-loader.ts
│   │   │   └── backend-api.ts  # Backend API client
│   │   └── types/             # TypeScript types
│   ├── Dockerfile             # Frontend container config
│   └── package.json
│
├── docker-compose.yml         # Multi-container orchestration
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
└── ARCHITECTURE.md           # This file
```

---

## 🔄 Data Flow

### Game Flow (Normal Play)
```
1. User types letter
   ↓
2. Zustand Store → Update currentGuess
   ↓
3. User presses Enter
   ↓
4. submitGuess() → evaluateGuess()
   ↓
5. Update state (guesses, evaluations, keyboard)
   ↓
6. Re-render GameBoard (animation)
   ↓
7. Check win/lose condition
```

### Agent Flow (Auto Solve)
```
1. User clicks "Agent" button
   ↓
2. useAgentSolver.runAgent()
   ↓
3. Check Backend health
   ├─ ✅ Healthy → Use Backend API
   │   ├─ POST /api/solve
   │   ├─ Receive next guess
   │   └─ Submit to game
   │
   └─ ❌ Down → Use Client-side solver
       ├─ Load words.txt
       ├─ DFS algorithm
       └─ Submit to game
   ↓
4. Repeat until win/lose (max 6 attempts)
```

---

## 🎯 Backend API Endpoints

### Health & Info
- `GET /` - Service information
- `GET /health` - Health check

### Word Operations
- `POST /api/validate` - Validate if word exists
- `GET /api/words/stats` - Letter frequency analysis
- `GET /api/words/random` - Get random word
- `GET /api/words/daily` - Get daily word (deterministic)

### Agent Solver
- `POST /api/solve` - Get next best guess
  - Input: Previous guesses & evaluations
  - Output: Next guess + confidence + remaining words

---

## 🧮 Agent Solver Algorithm (DFS)

### Strategy
```python
1. Initialize with full word list (14,855 words)

2. For each guess:
   a. Filter possible words based on all previous feedback
   b. Score remaining words by information gain
   c. Choose word with highest score
   d. Submit guess
   e. Get feedback (correct/present/absent)
   f. Update possible words list

3. Repeat until:
   - Word found (all correct)
   - Max attempts (6) reached
   - No valid words remaining
```

### Filtering Logic
```
For each previous guess:
  - Green (correct): Word MUST have letter at exact position
  - Yellow (present): Word MUST have letter but NOT at that position
  - Gray (absent): Word MUST NOT have letter (unless correct/present elsewhere)
```

### Scoring Heuristic
```
Score = Σ(letter_frequency) + 2 × Σ(position_frequency)

Prefer words with:
  1. Common letters in remaining words
  2. Letters at common positions
  3. Diverse unique letters (first guess)
```

### Example Execution
```
Attempt 1: AROSE (starter word)
  → Feedback: [⬛,⬛,⬛,🟨,⬛]
  → Filter: 14,855 → 527 words (has S, no A/R/O/E)

Attempt 2: SLING (high score from 527)
  → Feedback: [🟩,⬛,⬛,⬛,⬛]
  → Filter: 527 → 23 words (S at pos 0, no L/I/N/G)

Attempt 3: SQUAD (best from 23)
  → Feedback: [🟩,🟩,🟩,🟩,🟩]
  → WIN! 🎉
```

---

## 🔐 Security & Performance

### CORS Configuration
```python
allow_origins = [
  "http://localhost:3000",    # Dev
  "http://frontend:3000"      # Docker
]
```

### Performance Optimization
- **Word list caching:** Loaded once on startup
- **Scoring sample limit:** Max 100 words evaluated per guess
- **Client-side fallback:** Reduces backend dependency
- **Async processing:** Non-blocking agent execution

### Data Validation
- Word length check (5 letters)
- Uppercase normalization
- Valid characters (A-Z only)

---

## 🐳 Docker Architecture

### Services
```yaml
services:
  backend:
    - Port: 8000
    - Language: Python 3.11
    - Framework: FastAPI + Uvicorn
    - Health check enabled
    
  frontend:
    - Port: 3000
    - Framework: Next.js 16
    - Environment: NEXT_PUBLIC_API_URL
    - Depends on: backend
```

### Network
```
Docker Network (bridge):
  frontend:3000 ←→ backend:8000
  
External Access:
  localhost:3000 → frontend
  localhost:8000 → backend
```

---

## 📊 State Management

### Zustand Store (game-store.ts)
```typescript
State:
  - answer: string              // Target word
  - guesses: string[]           // Submitted guesses
  - evaluations: LetterState[][]// Feedback for each guess
  - currentGuess: string        // Current input
  - keyboard: KeyboardState     // Letter states for UI
  - isGameOver: boolean
  - isWinner: boolean
  - score: number

Actions:
  - startNewGame()
  - handleKey()
  - submitGuess()
  - submitAgentGuess()
```

### LocalStorage Persistence
```typescript
Persisted:
  - mode (daily/random)
  - solutionId
  - score

Not Persisted:
  - guesses (reset each game)
  - evaluations
  - currentGuess
```

---

## 🎨 UI Components

### Component Hierarchy
```
WordlyMain
├─ GameHeader
├─ GameBoard
│  └─ GameTile × 30 (6 rows × 5 cols)
├─ AttemptsCounter
├─ GameControls
│  ├─ New Game Button
│  ├─ Agent Button
│  └─ Stats Button
├─ OnscreenKeyboard
├─ GameOverModal
└─ StatsModal
```

### State Colors
- Empty: White (`bg-white`)
- Filled: Light blue (`bg-primary-50`)
- Correct: Green (`bg-emerald-500`)
- Present: Yellow (`bg-amber-500`)
- Absent: Gray (`bg-neutral-500`)

---

## 🚀 Deployment

### Development
```bash
# Backend
cd Backend && uvicorn main:app --reload

# Frontend
cd FrontEnd && npm run dev
```

### Production (Docker)
```bash
docker-compose up --build
```

### Environment Variables
```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend
PYTHONUNBUFFERED=1
```

---

## 📈 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication
- [ ] Global leaderboard
- [ ] Multiplayer mode
- [ ] Websocket for real-time updates
- [ ] Advanced AI models (ML-based solver)
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Rate limiting
- [ ] Caching layer (Redis)

---

## 🧪 Testing

### Backend Testing
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

### Frontend Testing
```bash
# Development
npm run dev

# Build
npm run build
npm start
```

### Integration Testing
```bash
# Full stack
docker-compose up
# Test at localhost:3000
```
