import shutil
from pathlib import Path

def copy_to_process(src_path: Path, dest_dir: Path) -> Path:
    """Copy a file from source to the process directory."""
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src_path}")
    
    dest_path = dest_dir / src_path.name
    shutil.copy2(src_path, dest_path)
    return dest_path

def move_to_finish(src_path: Path, dest_dir: Path) -> Path:
    """Move a file from process to the finish directory (category folder)."""
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    dest_path = dest_dir / src_path.name
    shutil.move(src_path, dest_path)
    return dest_path

def rename_file(src_path: Path, new_name: Path) -> Path:
    """Rename a file in place."""
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    dest_path = src_path.parent / new_name
    src_path.rename(dest_path)
    return dest_path
