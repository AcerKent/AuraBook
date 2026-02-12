import subprocess
import shutil
from pathlib import Path

def convert_epub_to_pdf(input_path: Path, output_dir: Path) -> Path:
    """
    Convert an EPUB file to PDF using ebook-convert (Calibre).
    
    Args:
        input_path (Path): Path to the source EPUB file.
        output_dir (Path): Directory where the PDF should be saved.
        
    Returns:
        Path: Path to the generated PDF file, or None if conversion failed.
    """
    if not shutil.which("ebook-convert"):
        print("Error: ebook-convert not found. Please install Calibre and add it to PATH.")
        return None

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        filename_no_ext = input_path.stem
        output_path = output_dir / f"{filename_no_ext}.pdf"
        
        # Determine command based on OS? unique command usually works if in PATH
        # ebook-convert input_file output_file [options]
        
        cmd = [
            "ebook-convert",
            str(input_path),
            str(output_path),
            "--paper-size", "a4",
            "--pdf-page-numbers"
            # Add more options here if needed, e.g., margins
        ]
        
        # Run conversion, capturing output to avoid cluttering main progress bar unless error
        # Use text=False (default) to get bytes, then decode safely to avoid UnicodeDecodeError on Windows (CP950)
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            check=False
        )
        
        if result.returncode == 0 and output_path.exists():
            return output_path
        else:
            # Decode stderr safely
            error_msg = result.stderr.decode('utf-8', errors='replace') if result.stderr else "Unknown error"
            print(f"Conversion failed for {input_path.name}: {error_msg}")
            return None
            
    except Exception as e:
        print(f"Exception during conversion: {e}")
        return None
