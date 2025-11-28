import base64, io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from google.genai import types
from src.app.config import DEFAULT_PERSON_B64, DEFAULT_CLOTHES_B64
from PIL import Image

from src.app.client import get_client
from src.app.models import ImageGenerationRequest, ImageGenerationResponse

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/generate", response_model=ImageGenerationResponse)
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
                request.prompt,
                # add the image of the person here
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

                print(base64_image)
                image = Image.open(io.BytesIO(image_bytes))
                image.show()
                break

        print(response)

        # return StreamingResponse(
        #     iter([response.candidates[0].content.parts[0].inline_data.data]),
        #     media_type="image/png",
        #     headers={"Content-Disposition": "attachment; filename=generated_image.png"},
        # )
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
