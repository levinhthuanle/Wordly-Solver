# Wordly Solver - Frontend

A simple, modern, interactive Wordle game interface with AI-powered features.

This is adapted from an existing Wordle implementation, redesigned for an application-based layout with integrated AI solver capabilities.

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app router
│   │   ├── page.tsx           # Main game page
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css        # Global styles
│   │   ├── scores/            # Scores pages
│   │   └── (..)scores/        # Parallel route modal
│   ├── components/             # React components
│   │   ├── GameBoard.tsx      # Main game grid
│   │   ├── GameTile.tsx       # Individual letter tiles
│   │   ├── AISuggestionPanel.tsx     # AI helper panel
│   │   ├── AutoplayPanel.tsx         # Autoplay controls
│   │   ├── AutoplayTranscriptModal.tsx
│   │   ├── GameOverModal.tsx
│   │   ├── StatsModal.tsx
│   │   ├── keyboard/
│   │   │   └── OnscreenKeyboard.tsx
│   │   └── ...
│   ├── hooks/                  # Custom React hooks
│   │   ├── useGameController.ts
│   │   ├── useAISuggestions.ts
│   │   ├── useAutoplay.ts
│   │   ├── useGameStats.ts
│   │   └── useScores.ts
│   ├── stores/                 # Zustand state management
│   │   └── game-store.ts
│   ├── types/                  # TypeScript definitions
│   │   └── types.ts
│   ├── utils/                  # Utility functions
│   │   ├── api-utils.ts       # Backend API client
│   │   ├── game-utils.ts      # Game logic
│   │   ├── stats-utils.ts     # Statistics helpers
│   │   └── word-loader.ts     # Word list management
│   └── constants/
│       └── constants.ts        # App-wide constants
├── public/
│   └── wordlist.json          # 10,000+ valid words
├── next.config.mjs            # Next.js configuration
├── tailwind.config.js         # Tailwind CSS config
├── tsconfig.json              # TypeScript config
└── Dockerfile                 # Production container
```

## Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

```

Open [http://localhost:3000](http://localhost:3000) to play the game. It's recommended to run the backend alongside to enable AI suggestion features.

### Environment Variables

Create a `.env.local` file (optional):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```
## Docker

**Note:** The following Docker instructions are AI-generated. Please verify before use.

### Build and Run

```bash
# Build the image
docker build -t wordly-solver-frontend .

# Run the container
docker run -p 3000:3000 wordly-solver-frontend
```

### Docker Compose (Recommended)

```bash
# From project root with both frontend and backend
docker-compose up --build
```

The Dockerfile uses:
- Multi-stage builds for optimal image size
- Standalone output mode for minimal dependencies
- Non-root user for security
- Health checks for monitoring

## Development Tips

### Hot Reload
The development server includes hot module replacement for instant updates during development.

### Type Checking
```bash
# Run TypeScript type checker
npx tsc --noEmit
```