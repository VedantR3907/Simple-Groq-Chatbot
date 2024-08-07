import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

GROQ_CLIENT = AsyncGroq(api_key = os.environ.get("GROQ_API_KEY"))