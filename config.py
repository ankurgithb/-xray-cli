import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
INSTRUCTIONS = "You are a clear, practical Python and AI engineering tutor."
MAX_CONTEXT_MESSAGES = 6
MAX_OUTPUT_TOKENS = 1500

if not API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env file.")