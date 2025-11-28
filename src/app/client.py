"""
Gemini client initialization and management.
"""

import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client (singleton)
_client = None


def get_client():
    """Get or create the Gemini client instance"""
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client
