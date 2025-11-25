# Wordly-Solver

A Wordle-style word guessing game built with Next.js and Docker.

## Features

- 🎮 Random word selection from 14,855+ words
- 🎯 Daily challenge mode
- 📊 Statistics tracking
- ⌨️ Keyboard support
- 🎨 Beautiful UI with animations

## Word List

The game randomly selects words from `words.txt` which contains over 14,855 five-letter words.

## How to Run

### Method 1: Using Docker Compose (Recommended)

```bash
# Make sure Docker Desktop is running
docker-compose up --build
```

Access the game at: http://localhost:3000

### Method 2: Development Mode

```bash
cd FrontEnd
npm install
npm run dev
```

Access the game at: http://localhost:3000

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

## Game Rules

1. Guess the 5-letter word in 6 attempts
2. Green = Correct letter in correct position
3. Yellow = Correct letter in wrong position
4. Gray = Letter not in word

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Deployment**: Docker, Docker Compose
