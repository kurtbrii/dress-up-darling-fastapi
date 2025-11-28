import os

from fastapi import APIRouter

from src.app.config import __version__
from src.app.models import HealthCheckResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint - verifies API key is configured"""
    gemini_key_configured = bool(os.getenv("GEMINI_API_KEY"))
    
    status = "healthy" if gemini_key_configured else "degraded"
    
    return {
        "status": status,
        "version": __version__,
    }
