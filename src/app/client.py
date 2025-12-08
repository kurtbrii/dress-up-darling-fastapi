"""
Gemini client initialization and management.
"""

import os
from dotenv import load_dotenv
from google.genai import Client

# Load environment variables
load_dotenv()

# Cache Gemini clients by API key
_clients = {}


def get_client(api_key: str) -> Client:
    """Get or create the Gemini client instance for the given API key"""
    global _clients
    if api_key not in _clients:
        _clients[api_key] = Client(api_key=api_key)
    return _clients[api_key]
