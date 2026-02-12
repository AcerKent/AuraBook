from pathlib import Path
from typing import Optional
import ebooklib
from ebooklib import epub
from datetime import datetime
import warnings

# Suppress ebooklib warnings about future XML handling
warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib")
warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib")

def extract_epub_metadata(file_path: Path) -> dict:
    """
    Extract metadata from EPUB.
    Returns: {'date': 'YYYYMMDD'|None, 'publisher': str|None}
    """
    metadata = {'date': None, 'publisher': None}
    
    try:
        book = epub.read_epub(str(file_path), options={"ignore_ncx": True})
        
        # 1. Get Date
        dates = book.get_metadata('DC', 'date')
        if dates and dates[0][0]:
            date_str = dates[0][0].split('T')[0]
            if len(date_str) == 4 and date_str.isdigit():
                metadata['date'] = f"{date_str}0101"
            else:
                try:
                    metadata['date'] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")
                except ValueError:
                    try:
                        metadata['date'] = datetime.strptime(date_str, "%Y-%m").strftime("%Y%m01")
                    except ValueError:
                        pass

        # 2. Get Publisher (Category)
        publishers = book.get_metadata('DC', 'publisher')
        if publishers:
            # Prefer the first publisher
            for pub in publishers:
                p = pub[0]
                if p and isinstance(p, str):
                    # Clean up publisher name if needed
                    metadata['publisher'] = p.strip()
                    break
        
        # 3. Get Author (Creator)
        creators = book.get_metadata('DC', 'creator')
        if creators:
            for creator in creators:
                c = creator[0]
                if c and isinstance(c, str):
                    metadata['author'] = c.strip()
                    break
        
        return metadata
        
    except Exception as e:
        # print(f"Error reading EPUB metadata from {file_path.name}: {e}")
        return metadata
