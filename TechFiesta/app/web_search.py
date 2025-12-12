import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("Missing SERPER_API_KEY in .env file")

SEARCH_URL = "https://google.serper.dev/search"


def fetch_web_snippets(query: str, max_results: int = 5) -> list[str]:
    """
    Sends the query to Serper.dev and retrieves web snippets.
    Automatically trims long queries to avoid API issues.
    """

    if len(query) > 280:
        query = query[:280]  # Hard safety limit for Serper

    payload = {
        "q": query,
        "num": max_results
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(SEARCH_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract organic search results
        snippets = []
        for item in data.get("organic", []):
            text = item.get("snippet") or item.get("title")
            if text and text.strip():
                snippets.append(text.strip())

        return snippets

    except Exception as e:
        print("Error fetching Serper.dev results:", e)
        return []
