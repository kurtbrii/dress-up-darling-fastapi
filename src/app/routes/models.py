from fastapi import APIRouter

from src.app.client import get_client
from src.app.models import ModelsResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=ModelsResponse)
async def list_models():
    """List all available Gemini models"""
    client = get_client()
    models = []

    try:
        for m in client.models.list():
            model_name = m.model_dump().get("name")
            models.append(model_name)

        return {
            "status": "success",
            "models": models,
        }
    except Exception as e:
        return {
            "status": "error",
            "models": [],
            "message": str(e),
        }
