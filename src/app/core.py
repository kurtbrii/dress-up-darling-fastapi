"""
FastAPI application factory and configuration.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.routes import health, images, models


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    print("🚀 FastAPI application starting...")
    yield
    # Shutdown
    print("🛑 FastAPI application shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Dress Up Darling API",
        description="AI-powered image generation API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(health.router)
    app.include_router(images.router)
    app.include_router(models.router)

    @app.get("/")
    async def root():
        """Root endpoint - welcome message"""
        return {
            "message": "Welcome to Dress Up Darling API",
            "status": "healthy",
            "docs": "/docs",
        }

    return app
