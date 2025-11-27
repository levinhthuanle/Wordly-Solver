# Wordly Solver Backend

Modern FastAPI backend cho Wordly puzzle solver.

## Cấu trúc

```
Backend/
├── src/
│   └── backend/          # Main package
│       ├── main.py       # FastAPI app
│       ├── schema.py     # Pydantic models
│       ├── agent.py      # Solver logic
│       ├── api/
│       │   └── routes.py # API endpoints
│       └── data/
│           └── wordlist.json
├── algorithms/           # AI algorithms
│   ├── dfs_algorithm.py
│   ├── hill_climbing_algorithm.py
│   └── simulated_annealing_algorithm.py
├── pyproject.toml        # Dependencies
└── uv.lock              # Lock file
```

## Quick Start

```bash
# Install dependencies với uv (khuyến nghị)
uv pip install -e .

# Hoặc với pip
pip install -e .

# Chạy development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/solve` - Nhận gợi ý từ tiếp theo
- `POST /api/validate` - Kiểm tra từ hợp lệ
- `GET /api/words/all` - Lấy tất cả từ hợp lệ
- `GET /health` - Health check

Xem main README để biết chi tiết API documentation.

## Testing

```bash
python test_backend.py
```

## Docker

```bash
# Build và chạy
docker-compose up -d --build backend

# Xem logs
docker logs wordly-solver-backend-1
```
