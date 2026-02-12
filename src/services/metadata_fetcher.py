import requests
from typing import Optional

def fetch_publication_date(title: str) -> Optional[str]:
    """
    Search for the publication date of a book using Open Library API.
    Returns: 'YYYYMMDD' string or None if not found/error.
    """
    if not title:
        return None
        
    search_url = "https://openlibrary.org/search.json"
    params = {
        "title": title,
        "fields": "first_publish_year,publish_date",
        "limit": 1
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("docs"):
            return None
            
        book = data["docs"][0]
        
        # Prefer first_publish_year
        if "first_publish_year" in book:
            return f"{book['first_publish_year']}0101" # Default to Jan 1st
            
        # Fallback to publish_date
        if "publish_date" in book and book["publish_date"]:
            # This can be varied formats, keeping it simple for now or returning None if complex
            # For this MVP, let's stick to year if possible
            return None 
            
        return None
        
    except Exception as e:
        print(f"Error fetching metadata for '{title}': {e}")
        return None
