"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional



class ValidateRequest(BaseModel):
    """Request to validate a word."""
    word: str = Field(min_length=5, max_length=5, description="5-letter word to validate")


class ValidateResponse(BaseModel):
    """Response for word validation."""
    word: str
    valid: bool
    message: str


