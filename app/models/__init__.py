"""Models package - Contains Pydantic schemas and constants."""

from .schemas import ChatRequest, ChatResponse, PredictionRequest, PredictionResponse
from .constants import (
    EMERGENCY_KEYWORDS,
    UNSAFE_KEYWORDS,
    HEALTH_RELATED_KEYWORDS,
    OFF_TOPIC_KEYWORDS,
    SYSTEM_PROMPT,
    TOPIC_VALIDATION_PROMPT,
)

__all__ = [
    "ChatRequest",
    "ChatResponse",
    "PredictionRequest",
    "PredictionResponse",
    "EMERGENCY_KEYWORDS",
    "UNSAFE_KEYWORDS",
    "HEALTH_RELATED_KEYWORDS",
    "OFF_TOPIC_KEYWORDS",
    "SYSTEM_PROMPT",
    "TOPIC_VALIDATION_PROMPT",
]
