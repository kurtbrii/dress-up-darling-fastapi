"""
Application configuration and constants.
"""

__version__ = "0.1.0"


import base64
from pathlib import Path


def load_image_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


DEFAULT_PERSON_B64 = load_image_b64("assets/person.jpg")
DEFAULT_CLOTHES_B64 = load_image_b64("assets/clothes.jpeg")
