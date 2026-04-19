import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
POLYMARKET_API_URL = os.getenv("POLYMARKET_API_URL", "https://gamma-api.polymarket.com")
KALSHI_API_URL = os.getenv("KALSHI_API_URL", "https://trading-api.kalshi.com/trade-api/v2")

LLM_MODEL = "mistralai/mistral-7b-instruct:free"