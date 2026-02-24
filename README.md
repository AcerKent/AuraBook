# AuraBook

An automated tool to organize, rename, and convert your e-book library. It scans for EPUB files, extracts metadata (Author, Publisher, Date), renames them for consistency, categorizes them by publisher, and automatically converts them to PDF.

## Features

- **Recursive Scanning**: Finds EPUB files in `input/` and all its subdirectories.
- **Smart Renaming**: `YYYYMMDD_Title_Author.epub`
    - Extracts publication date and author from EPUB metadata.
    - Falls back to Open Library API if local metadata is missing.
- **Publisher Categorization**: Moves files to `finish/epub/<Publisher Name>/`.
- **Auto-Conversion**: Converts processed EPUBs to PDF using Calibre's `ebook-convert`.
    - PDFs are saved to `finish/pdf/<Publisher Name>/`.
    - Configurable font size via `--font-size` (default: 20pt).
    - Activity-based timeout: only kills conversion if no progress for 120 seconds.
    - Real-time conversion progress display.
- **Custom Paths**: Specify custom input/output directories via CLI arguments.
- **Per-File Timing**: Logs processing time for each file.
- **Execution Summary**: Color-coded report with failed file details.
- **Automated Execution**: Includes a batch script for background runs via Windows Task Scheduler.

## Prerequisites

- **Python 3.10+**
- **Calibre**: Required for `ebook-convert` (PDF conversion). Ensure it's in your system PATH.

## Installation

1.  **Clone the repository** (or download the source).
2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Options
```bash
# Default (uses input/ and finish/ directories)
python main.py

# Specify custom input and output directories
python main.py --input "D:\Books\new_epubs" --output "D:\Archive"

# Specify PDF font size (in points)
python main.py --font-size 16

# All options combined
python main.py --input "D:\Books" --output "D:\Archive" --font-size 14
```

| Argument | Description | Default |
|---|---|---|
| `--input` | Input directory containing EPUB files | `input/` |
| `--output` | Output directory for processed files | `finish/` |
| `--font-size` | PDF default font size in points | `20` |

### Automated Execution (Background)
Double-click `run_auto.bat`. This script uses the configured Python environment to run the processor without user intervention.

## Project Structure

See [docs/CODEMAPS/INDEX.md](docs/CODEMAPS/INDEX.md) for a detailed architectural overview.

## License
Proprietary / Private Use
