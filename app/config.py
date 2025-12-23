"""Configuration management for YTSumAI"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DOWNLOAD_DIR = BASE_DIR / os.getenv("DOWNLOAD_DIR", "downloads")

# Ensure directories exist
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "llama3.1:8b-instruct-q4_K_M")

# Processing limits
MAX_VIDEO_DURATION = int(os.getenv("MAX_VIDEO_DURATION", "7200"))  # 2 hours
CHUNK_DURATION_MINUTES = int(os.getenv("CHUNK_DURATION_MINUTES", "30"))

# Audio settings
AUDIO_FORMAT = "mp3"
AUDIO_BITRATE = "128k"

# Summarization settings
MAX_SUMMARY_LENGTH = 500  # words
CHUNK_OVERLAP = 100  # words for overlap between chunks
