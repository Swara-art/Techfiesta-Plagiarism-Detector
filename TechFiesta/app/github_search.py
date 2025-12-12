import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in environment variables.")

GITHUB_SEARCH_URL = "https://api.github.com/search/code"

def search_github_code(query: str, language: str = None, max_results: int = 5):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    q = query
    if language:
        q += f" language:{language}"

    params = {
        "q": q,
        "per_page": max_results,
    }

    response = requests.get(GITHUB_SEARCH_URL, headers=headers, params=params)

    if response.status_code != 200:
        print("GitHub search failed:", response.text)
        return []

    items = response.json().get("items", [])
    return items

def fetch_raw_file(download_url: str) -> str:
    """
    Download raw GitHub file contents.
    """
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print("Error fetching raw GitHub file:", e)

    return ""


        