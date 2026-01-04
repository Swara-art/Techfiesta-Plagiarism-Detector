import json
import wikipedia
from pathlib import Path

TOPICS_FILE = "wiki_topics.json"
OUTPUT_DIR = Path("data/corpus")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    topics_by_domain = json.load(f)

for domain, topics in topics_by_domain.items():
    domain_dir = OUTPUT_DIR / domain
    domain_dir.mkdir(exist_ok=True)

    for topic in topics:
        try:
            print(f"Downloading: {topic}")
            page = wikipedia.page(topic, auto_suggest=False)

            file_name = topic.replace(" ", "_").lower() + ".txt"
            file_path = domain_dir / file_name

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page.content)

            print(f"Saved to {file_path}")

        except wikipedia.DisambiguationError as e:
            print(f"Skipping ambiguous topic: {topic}")

        except Exception as e:
            print(f"Failed for {topic}: {e}")

print("Wikipedia corpus download complete")
