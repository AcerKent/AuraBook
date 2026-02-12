import pytest
import shutil
from pathlib import Path

@pytest.fixture
def temp_dirs(tmp_path):
    """Create temporary directories for input, process, and finish."""
    base_dir = tmp_path / "ebook_archiver"
    input_dir = base_dir / "input"
    process_dir = base_dir / "process"
    finish_dir = base_dir / "finish"
    
    input_dir.mkdir(parents=True)
    process_dir.mkdir(parents=True)
    finish_dir.mkdir(parents=True)
    
    return {
        "input": input_dir,
        "process": process_dir,
        "finish": finish_dir,
        "root": base_dir
    }

@pytest.fixture
def sample_file(temp_dirs):
    """Create a sample dummy file in the input directory."""
    input_dir = temp_dirs["input"]
    file_path = input_dir / "apk.tw_Investing_101.txt"
    file_path.write_text("Dummy content")
    return file_path
