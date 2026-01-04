import os

def extract_text_from_assignment(assignment_dir: str) -> str:
    if not os.path.exists(assignment_dir):
        return ""

    files = [
        f for f in os.listdir(assignment_dir)
        if f.lower().endswith(".txt")
    ]

    if not files:
        print("No .txt files found in assignment folder")
        return ""

    path = os.path.join(assignment_dir, files[0])
    print(f"Reading file: {path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()
    

