import requests
from bs4 import BeautifulSoup

HEADERS={
    "User-Agent": "Mozilla/5.0" 
}

def duckduckgo_search(query: str, max_results: int = 5):
    url = f"https://duckduckgo.com/html/"
    data = {"q": {query}}
    
    response = requests.post(url, data=data, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    snippets = []
    for result in soup.select(".result__snippet"):
        if len(snippets) >= max_results:
            break
        snippets.append(result.text.strip())

    return snippets