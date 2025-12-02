# google_books.py
import os, requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "").strip()

BASE = "https://www.googleapis.com/books/v1/volumes"

def search_google_books(q: str, max_results: int = 8):
    params = {"q": q, "maxResults": max_results}
    if API_KEY:
        params["key"] = API_KEY
    r = requests.get(BASE, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    out = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        authors = info.get("authors") or []
        out.append({
            "external_id": item.get("id"),
            "title": info.get("title"),
            "author": ", ".join(authors) if authors else None,
            "description": info.get("description"),
            "cover_image": info.get("imageLinks", {}).get("thumbnail") if info.get("imageLinks") else None,
            "category": (info.get("categories") or [None])[0]
        })
    return out
