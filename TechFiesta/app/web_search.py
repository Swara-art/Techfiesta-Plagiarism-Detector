from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Add to your .env file

if not TAVILY_API_KEY:
    raise ValueError("Missing TAVILY_API_KEY in environment variables")

client = TavilyClient(api_key=TAVILY_API_KEY)


def fetch_web_snippets(query: str, max_results: int = 5) -> list[str]:
    """
    Takes a sentence and returns web search snippets
    that are semantically similar.
    """
    try:
        response = client.search(
            query=query,
            search_depth="advanced",    # gives better content
            max_results=max_results,    # how many pages
        )

        corpus = []
        for item in response.get("results", []):
            # Tavily gives: "content", "snippet", "title"
            text = item.get("content") or item.get("snippet") or ""
            if text.strip():
                corpus.append(text)

        return corpus

    except Exception as e:
        print("Error fetching web results:", e)
        return []
