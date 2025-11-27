"""Modern FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import router


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="Wordly Solver API",
        version="2.0.0",
        description="Modern AI-powered Wordle solver with multiple algorithms"
    )
    
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://frontend:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router)
    
    @app.get("/")
    async def root():
        return {
            "service": "Wordly Solver API",
            "version": "2.0.0",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "solve": "/api/solve",
                "validate": "/api/validate",
                "wordlist": "/api/words/all"
            }
        }
    
    return app


app = create_app()
