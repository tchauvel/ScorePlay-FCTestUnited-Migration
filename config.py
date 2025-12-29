"""Configuration settings for ScorePlay migration agent."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("SCOREPLAY_API_BASE_URL", "https://dc.scoreplay.io/api")
API_KEY = os.getenv("SCOREPLAY_API_KEY", "")
API_URL = f"{API_BASE_URL}/assets"

# Source directory
SOURCE_PATH = os.getenv("SOURCE_PATH", "./videos")
SOURCE = Path(SOURCE_PATH)

# Request headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Filename pattern
FILENAME_PATTERN = r"^(?P<m>M\d+)_(?P<p>P\d+)_(?P<t>\d{8}T\d{6})$"


# Request timeout (seconds)
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Validate required configuration
if not API_KEY:
    raise ValueError("SCOREPLAY_API_KEY is required. Set it in .env file or environment variable.")

