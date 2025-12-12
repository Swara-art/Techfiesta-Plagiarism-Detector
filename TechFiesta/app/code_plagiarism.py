from app.github_search import search_github_code, fetch_raw_file
from app.code_similarity import compute_code_plagiarism
import ast

def extract_keywords(text: str, max_keywords: int = 5) -> list:
    try:
        tree = ast.parse(text)
        tokens = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                tokens.append(node.name)
            if isinstance(node, ast.ClassDef):
                tokens.append(node.name)

        if not tokens:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            tokens = lines[:5]

        return tokens[:3]
    except:
        return text.split()[:3]


def detect_github_plagiarism(code: str, language="python"):
    keywords = extract_keywords(code)

    github_snippets = []

    for kw in keywords:
        results = search_github_code(kw, language=language)
        for item in results:
            raw_url = item.get("html_url").replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob/", "/")

            raw_code = fetch_raw_file(raw_url)
            if raw_code:
                github_snippets.append(raw_code)

    if not github_snippets:
        return {
            "found": False,
            "plagiarism_score": 0,
            "details": [],
            "message": "No similar code found on GitHub."
        }

    block_results = []
    max_score = 0

    for snippet in github_snippets:
        res = compute_code_plagiarism(code, snippet)
        block_results.append(res)
        max_score = max(max_score, res["plagiarism_score"])

    return {
        "found": max_score > 10,
        "plagiarism_score": max_score,
        "details": block_results,
        "total_github_files_checked": len(github_snippets)
    }
