import sys
import warnings
from pathlib import Path
from ebooklib import epub

# Suppress ebooklib warnings
warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib")
warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib")

def print_metadata(file_path):
    try:
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}")
            return

        print(f"--- Metadata for: {file_path} ---")
        book = epub.read_epub(file_path, options={"ignore_ncx": True})
        
        # Print all DC metadata
        for namespace, meta_dict in book.metadata.items():
            print(f"\nNamespace: {namespace}")
            for key, values in meta_dict.items():
                print(f"  {key}:")
                for v in values:
                    # Value is usually a tuple (value, attributes)
                    val = v[0] if isinstance(v, tuple) else v
                    print(f"    - {val}")
                    
        print("\n--- End of Metadata ---")
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_epub.py <path_to_epub_file_or_directory>")
        sys.exit(1)
        
    target_path = Path(sys.argv[1])
    
    if target_path.is_dir():
        epub_files = list(target_path.glob("*.epub"))
        print(f"Found {len(epub_files)} EPUB files in directory: {target_path}\n")
        print("="*60)
        
        for i, file_path in enumerate(epub_files, 1):
            print(f"File {i}/{len(epub_files)}")
            print_metadata(file_path)
            print("\n" + "="*60 + "\n")
    else:
        print_metadata(target_path)
