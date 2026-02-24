import time
from pathlib import Path
from src.core.config import INPUT_DIR, PROCESS_DIR, FINISH_DIR, ensure_directories
from src.services.cleaner import clean_filename
from src.services.metadata_fetcher import fetch_publication_date
from src.services.categorizer import categorize_book
from src.utils.file_ops import copy_to_process, move_to_finish, rename_file
from src.services.epub_parser import extract_epub_metadata
from src.services.converter import convert_epub_to_pdf
from tqdm import tqdm

def process_workflow(input_dir=None):
    """Main workflow to process books."""
    ensure_directories()
    
    # Use custom input_dir if provided, otherwise fall back to config default
    scan_dir = input_dir if input_dir else INPUT_DIR
    
    # Get all files first to allow tqdm to show total progress
    # Use rglob('*') to find all files recursively in subdirectories
    files_to_process = [f for f in scan_dir.rglob("*") if f.is_file() and f.name != ".gitkeep"]
    
    if not files_to_process:
        print(f"No files found in {scan_dir} (recursive scan).")
        return

    # Statistics
    stats = {
        'total': len(files_to_process),
        'epub_success': 0,
        'pdf_success': 0,
        'errors': 0
    }

    # 1. Process files with progress bar
    with tqdm(files_to_process, unit="file") as pbar:
        for file_path in pbar:
            pbar.set_description(f"Processing {file_path.name}")
            try:
                start_time = time.time()
                process_path = copy_to_process(file_path, PROCESS_DIR)
                
                # 2. Clean filename
                clean_name = clean_filename(process_path.name)
                if clean_name != process_path.name:
                    process_path = rename_file(process_path, clean_name)
                    pbar.write(f"  Cleaned name: {clean_name}")
                
                # 3. Fetch Date (Local -> Web)
                pub_date = None
                epub_publisher = None
                
                if "_" not in process_path.stem or not process_path.stem.split("_", 1)[0].isdigit():
                    # Try local EPUB metadata first
                    if process_path.suffix.lower() == '.epub':
                        metadata = extract_epub_metadata(process_path)
                        pub_date = metadata['date']
                        epub_publisher = metadata['publisher']
                        epub_author = metadata.get('author')
                        
                        if pub_date:
                             pbar.write(f"  Found date within EPUB: {pub_date}")
                        if epub_publisher:
                             pbar.write(f"  Found publisher within EPUB: {epub_publisher}")
                        if epub_author:
                             pbar.write(f"  Found author within EPUB: {epub_author}")

                    # Fallback to web search for date if not found
                    if not pub_date:
                        pbar.set_description(f"Searching metadata for {process_path.stem}")
                        pub_date = fetch_publication_date(process_path.stem)
                        if pub_date:
                            pbar.write(f"  Found date online: {pub_date}")
                        else:
                            pbar.write(f"  Date not found for: {process_path.stem}")
                    
                    if pub_date:
                        # Construct new filename: Date_Title_Author.epub
                        base_name = process_path.stem
                        
                        # If author exists, append it
                        if epub_author:
                            # Sanitize author name for filename
                            safe_author = "".join(c for c in epub_author if c.isalnum() or c in (' ', '-', '_')).strip()
                            new_name = f"{pub_date}_{base_name}_{safe_author}{process_path.suffix}"
                        else:
                            new_name = f"{pub_date}_{process_path.name}"
                            
                        process_path = rename_file(process_path, new_name)
                        pbar.write(f"  Renamed: {new_name}")
                else:
                    pbar.write(f"  Date likely already present in: {process_path.name}")
                    pass
                
                # 4. Categorize & Move
                if epub_publisher:
                    category = epub_publisher
                    pbar.write(f"  Category from Publisher: {category}")
                else:
                    category = categorize_book(process_path.stem)
                    pbar.write(f"  Category from Keywords: {category}")
                
                dest_dir = FINISH_DIR / "epub" / category
                dest_dir.mkdir(exist_ok=True, parents=True)
                final_path = move_to_finish(process_path, dest_dir)
                pbar.write(f"✓ Moved to -> {dest_dir}\n")
                stats['epub_success'] += 1
                
                # 5. Convert to PDF
                # PDF Destination: finish/pdf/<Category>/
                pdf_dest_dir = FINISH_DIR / "pdf" / category
                pbar.write(f"  Converting to PDF...")
                pdf_path = convert_epub_to_pdf(final_path, pdf_dest_dir)
                
                if pdf_path:
                    pbar.write(f"✓ PDF Created -> {pdf_dest_dir}")
                    stats['pdf_success'] += 1
                else:
                    pbar.write(f"❌ PDF Conversion failed for {final_path.name}")
                
                elapsed = time.time() - start_time
                pbar.write(f"⏱ Processing time: {elapsed:.2f}s\n")
                
            except Exception as e:
                elapsed = time.time() - start_time
                pbar.write(f"❌ Error processing {file_path.name}: {e}")
                pbar.write(f"⏱ Processing time: {elapsed:.2f}s\n")
                stats['errors'] += 1

    # Print Summary
    print_summary(stats)

def print_summary(stats):
    """Print color-coded summary."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    print("\n" + "="*60)
    print(f"{BOLD}PROCESSING SUMMARY{RESET}")
    print("="*60)
    print(f"Total Files Found: {stats['total']}")
    
    # EPUB
    color_epub = GREEN if stats['epub_success'] == stats['total'] else (RED if stats['epub_success'] == 0 else BOLD)
    print(f"EPUB Processed:    {color_epub}{stats['epub_success']}{RESET}")
    
    # PDF
    color_pdf = GREEN if stats['pdf_success'] == stats['epub_success'] and stats['epub_success'] > 0 else (RED if stats['pdf_success'] == 0 else BOLD)
    print(f"PDF Converted:     {color_pdf}{stats['pdf_success']}{RESET}")
    
    # Errors
    if stats['errors'] > 0:
        print(f"Errors:            {RED}{stats['errors']}{RESET}")
    else:
        print(f"Errors:            {GREEN}0{RESET}")
    print("="*60 + "\n")

if __name__ == "__main__":
    process_workflow()
