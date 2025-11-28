import base64, io
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from google.genai import types
from src.app.config import DEFAULT_PERSON_B64, DEFAULT_CLOTHES_B64
from PIL import Image
from src.app.helpers.constants import PROMPT

from src.app.client import get_client
from src.app.models import ImageGenerationRequest, ImageGenerationResponse

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Generate an image using Gemini's image generation model.

    Parameters:
    - **prompt**: The text prompt for image generation
    - **aspect_ratio**: Image aspect ratio (default: "9:16")
    - **person_image_b64**: Base64 encoded image of the person (optional, uses default if not provided)
    - **clothes_image_b64**: Base64 encoded image of the clothing (optional, uses default if not provided)
    """
    client = get_client()

    try:
        # Use provided images or fallback to hardcoded defaults

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                PROMPT,
                Image.open(io.BytesIO(base64.b64decode(request.person_image_b64))),
                Image.open(io.BytesIO(base64.b64decode(request.clothes_image_b64))),
            ],
            config=types.GenerateContentConfig(
                image_config=types.ImageConfig(
                    aspect_ratio=request.aspect_ratio,
                )
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                base64_image = base64.b64encode(image_bytes).decode("utf-8")

                # ! for debugging purposes: show the image
                # image = Image.open(io.BytesIO(image_bytes))
                # image.show()

                return ImageGenerationResponse(
                    status="success",
                    generated_image_b64=base64_image,
                )
        return ImageGenerationResponse(
            status="error",
            message="Couldn't generate image. Please try again.",
        )

    except Exception as e:
        return ImageGenerationResponse(
            status="error",
            message=str(e),
        )
