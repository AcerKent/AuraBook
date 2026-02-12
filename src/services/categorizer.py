

# Simple keyword mapping for demonstration
KEYWORD_MAP = {
    "money": "Business",
    "investing": "Business",
    "finance": "Business",
    "stock": "Business",
    "market": "Business",
    "python": "Technology",
    "javascript": "Technology",
    "coding": "Technology",
    "programming": "Technology",
    "algorithm": "Technology",
    "history": "History",
    "war": "History",
    "empire": "History",
    "novel": "Fiction",
    "story": "Fiction",
    "harry potter": "Fiction",
    "health": "Health",
    "diet": "Health",
    "travel": "Travel",
    "guide": "Travel",
    "law": "Law",
    "education": "Education",
    "learning": "Education",
    "art": "Art",
    "design": "Art",
    "philosophy": "Philosophy",
    "psychology": "Psychology",
    "mind": "Psychology",
    "sport": "Sports",
    "comic": "Comics",
    "manga": "Comics"
}

def categorize_book(title: str) -> str:
    """Determine the category based on the book title."""
    title_lower = title.lower()
    
    for keyword, category in KEYWORD_MAP.items():
        if keyword in title_lower:
            return category
            
    return "Other"
