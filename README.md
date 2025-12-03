# 🎮 Wordly Solver

> **AI-Powered Wordle** – A minimal Wordle clone featuring intelligent solvers and detailed heuristics.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-00979D?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com/)

## Features

- **Interactive Gameplay:** Standard Wordle rules (5 letters, 6 tries).
- **AI Assistants:** Real-time suggestions with confidence scores and reasoning.
- **Advanced Analytics:** Win rates, streak tracking, autoplay, and performance distribution.
- **Production Ready:** Fully Dockerized for one-command deployment.

## Architecture

```text
Wordly-Solver/
├── backend/              # FastAPI, AI logic, and Solver engine
├── frontend/             # Next.js 16 UI and State management
└── docker-compose.yml    # Orchestration of backend and frontend services, for Docker deployment
```
Please refer to the `README.md` within the `backend` or `frontend` directories for specific architectural details.

## Quick Start
### Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)
- (Optional) [Node.js & npm](https://nodejs.org/) and [uv](https://docs.astral.sh/uv/) for manual setup.
### Docker (Recommended)

```bash
git clone https://github.com/levinhthuanle/Wordly-Solver.git
cd Wordly-Solver
docker-compose up -d
```

### Development Setup

<details>
<summary>Click to expand manual installation steps</summary>

**backend**

```bash
cd backend
uv sync --all-extras
uv run uvicorn backend.main:app --reload --port 8000
```

**frontend**

```bash
cd frontend
npm install && npm run dev
```

For the url endpoints, once the services are running, you can access them as follows:
| Service | URL | Description |
| :--- | :--- | :--- |
| **frontend** | `http://localhost:3000` | Game Interface |
| **backend** | `http://localhost:8000` | API & Documentation |
</details>


## 📄 License & Status

**Status:** Academic Project (No outside contributions accepted).
**License:** MIT - See [LICENSE](https://www.google.com/search?q=LICENSE).