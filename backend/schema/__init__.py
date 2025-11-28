from pydantic import BaseModel, Field
from .solve_request import *
from .solve_response import *
from .game_state import *
from .validate import *
from .autoplay import *

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    words_count: int
    timestamp: str