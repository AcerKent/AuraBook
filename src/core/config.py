import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_DIR = Path(os.getenv("INPUT_DIR", BASE_DIR / "input"))
PROCESS_DIR = Path(os.getenv("PROCESS_DIR", BASE_DIR / "process"))
FINISH_DIR = Path(os.getenv("FINISH_DIR", BASE_DIR / "finish"))

# Settings
IGNORE_PATTERNS = ["apk.tw_"]

# Settings
IGNORE_PATTERNS = ["apk.tw_"]

def ensure_directories():
    """Ensure all required directories exist."""
    INPUT_DIR.mkdir(exist_ok=True, parents=True)
    PROCESS_DIR.mkdir(exist_ok=True, parents=True)
    FINISH_DIR.mkdir(exist_ok=True, parents=True)
