import os
import requests
from dotenv import load_dotenv

load_dotenv()

SEARCHAPI_KEY = os.getenv("SEARCHAPI_KEY")

if not SEARCHAPI_KEY:
    raise ValueError("SEARCHAPI_KEY not found in environment variables")

SEARCH_URL = "https://www.searchapi.io/api/v1/search"

def fetch_web_snippets(query: str, num_results: int = 5):
    headers = {
        "Authorization": f"Bearer {SEARCHAPI_KEY}"
    }
    params = {
        "q": query,
        "engine": "google",
        "num": num_results
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data  = response.json()
        
        snippets = []
        for item in data.get("organic_results", []):
            snippet = item.get("snippet") or item.get("title")
            if snippet:
                snippets.append(snippet.strip())

        return snippets
    
    except Exception as e:
        print("Error fetching SearchAPI.io results:", e)
        return []
    