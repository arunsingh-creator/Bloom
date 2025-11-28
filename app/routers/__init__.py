"""Routers package - Contains API endpoint definitions."""

from .chatbot import router as chatbot_router
from .prediction import router as prediction_router
from .pcos import router as pcos_router

__all__ = [
    "chatbot_router",
    "prediction_router",
    "pcos_router",
]
