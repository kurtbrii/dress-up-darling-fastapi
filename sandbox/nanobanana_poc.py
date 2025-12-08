import os
from google import genai

from dotenv import load_dotenv
from google.genai import types
from PIL import Image
import base64
import io


load_dotenv()


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Create an image of this person wearing a banana costume",
        # I need a base 64 here
        Image.open("assets/person.jpg"),
    ],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="9:16",
        )
    ),
)


for part in response.candidates[0].content.parts:
    if part.inline_data:
        image_bytes = part.inline_data.data
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        image = Image.open(io.BytesIO(image_bytes))
        image.show()
        break
