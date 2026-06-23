import requests
import json
import os

ARTICLES = [
    "Machine learning", "Climate change", "Photosynthesis",
    "World War II", "Artificial intelligence", "Quantum computing",
    "Solar energy", "Electric vehicle", "Blockchain", "RNA"
]

def get_wiki_text(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "prop": "extracts",
        "exintro": True, "explaintext": True,
        "titles": title, "format": "json"
    }
    headers = {"User-Agent": "prompt-engineering-task/1.0 (learning project)"}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    r = r.json()
    page = next(iter(r["query"]["pages"].values()))
    return page.get("extract", "")

def fetch_and_save_all():
    articles = {}

    for title in ARTICLES:
        print(f"Fetching: {title}")
        text = get_wiki_text(title)

        words = text.split()
        if len(words) > 2000:
            text = " ".join(words[:2000])

        articles[title] = text
        print(f" -> Got {len(text.split())} words")

    output_path = os.path.join("data", "articles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
        
    print(f"\nDone! Saved {len(articles)} articles to {output_path}")
    return articles


if __name__ == "__main__":
    fetch_and_save_all()