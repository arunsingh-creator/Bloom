"""
Configuration and environment setup.
"""

import os
from pathlib import Path
from groq import Groq

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Get the project root directory (parent of app/)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, skip
    pass

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PORT = int(os.environ.get("PORT", 8000))

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Model configuration
MODEL_NAME = "llama-3.3-70b-versatile"  # Current recommended model

# Framework availability flag (set by ML module imports)
PYTORCH_AVAILABLE = False
