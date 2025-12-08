from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator



class ShotType(str, Enum):
    """Enum for supported shot types"""

    CLOSE_UP = "close_up"
    FULL_BODY = "full_body"

class AspectRatio(str, Enum):
    """Enum for supported aspect ratios"""

    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "4:3"
    WIDE = "16:9"


class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""

    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.PORTRAIT, description="Aspect ratio of the image"
    )
    person_image_b64: str = Field(
        default=None,
        description="Base64 encoded image of the person to dress up",
    )
    clothes_image_b64: str = Field(
        default=None,
        description="Base64 encoded image of the outfit / clothing reference",
    )
    api_key: str = Field(
        default=None,
        description="API key for the Gemini API",
    )

    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if not v or not v.strip():
            raise ValueError('API key is required')
        return v


class ImageGenerationResponse(BaseModel):
    """Response model for image generation"""

    status: str
    message: Optional[str] = None
    generated_image_b64: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Response model for health check"""

    status: str
    version: str


class ModelsResponse(BaseModel):
    """Response model for models list"""

    status: str
    models: list[str] = []
