import subprocess
import shutil
import threading
import time
from pathlib import Path

def convert_epub_to_pdf(input_path: Path, output_dir: Path, idle_timeout: int = 120, progress_callback=None) -> Path:
    """
    Convert an EPUB file to PDF using ebook-convert (Calibre).
    
    Uses activity-based timeout: only kills the process if no output
    is received for `idle_timeout` seconds. Actively converting files
    will never be interrupted.
    
    Args:
        input_path (Path): Path to the source EPUB file.
        output_dir (Path): Directory where the PDF should be saved.
        idle_timeout (int): Seconds of inactivity before killing the process.
        progress_callback: Optional callable(str) to report progress lines.
        
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
        
        cmd = [
            "ebook-convert",
            str(input_path),
            str(output_path),
            "--paper-size", "a4",
            "--pdf-page-numbers",
        ]
        
        # Use Popen with stdout streaming for activity detection
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        # Shared state for activity tracking
        last_activity = [time.time()]
        stdout_lines = []
        
        def read_stdout():
            """Read stdout line by line, updating last_activity timestamp."""
            for raw_line in iter(process.stdout.readline, b''):
                line = raw_line.decode('utf-8', errors='replace').strip()
                if line:
                    last_activity[0] = time.time()
                    stdout_lines.append(line)
                    # Report progress (e.g., "10% Converting input...")
                    if progress_callback and '%' in line:
                        progress_callback(f"  📄 {line}")
            process.stdout.close()
        
        # Start reader thread
        reader = threading.Thread(target=read_stdout, daemon=True)
        reader.start()
        
        # Monitor: wait for process to finish or idle timeout
        while process.poll() is None:
            idle_seconds = time.time() - last_activity[0]
            if idle_seconds > idle_timeout:
                process.kill()
                process.wait()
                print(f"⏱ Conversion killed after {idle_timeout}s of inactivity for {input_path.name}")
                return None
            time.sleep(1)
        
        reader.join(timeout=5)
        
        if process.returncode == 0 and output_path.exists():
            return output_path
        else:
            error_msg = process.stderr.read().decode('utf-8', errors='replace') if process.stderr else "Unknown error"
            process.stderr.close()
            print(f"Conversion failed for {input_path.name}: {error_msg}")
            return None
            
    except Exception as e:
        print(f"Exception during conversion: {e}")
        return None
