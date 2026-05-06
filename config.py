import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
GDRIVE_FILE_ID_1 = os.getenv("GDRIVE_FILE_ID_1", "1j5ElESYs4mkQQ-0laPy37ZPgvOLLHyVP")
GDRIVE_FILE_ID_2 = os.getenv("GDRIVE_FILE_ID_2", "1oOeLtcCqu73RFQMGaB7kmsBEUNyZEw3W")
TARGET_NICHE = os.getenv("TARGET_NICHE", "trading education")
TARGET_PRODUCT = os.getenv("TARGET_PRODUCT", "CrowdWisdomTrading")
TARGET_URL = os.getenv("TARGET_URL", "https://crowdwisdomtrading.com")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def get_llm():
    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
    )
