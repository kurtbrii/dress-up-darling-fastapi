"""
Dress Up Darling FastAPI Application

Main entry point for the FastAPI application.
Run with: uvicorn main:app --reload
"""

from src.app import create_app

# Create the FastAPI application
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
