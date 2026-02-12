# Everything Claude Code (Ebook Archiver)

An automated tool to organize, rename, and convert your e-book library. It scans for EPUB files, extracts metadata (Author, Publisher, Date), renames them for consistency, categorizes them by publisher, and automatically converts them to PDF.

## Features

- **Recursive Scanning**: Finds EPUB files in `input/` and all its subdirectories.
- **Smart Renaming**: `YYYYMMDD_Title_Author.epub`
    - Extracts publication date and author from EPUB metadata.
    - Falls back to Open Library API if local metadata is missing.
- **Publisher Categorization**: Moves files to `finish/epub/<Publisher Name>/`.
- **Auto-Conversion**: Converts processed EPUBs to PDF using Calibre's `ebook-convert`.
    - PDFs are saved to `finish/pdf/<Publisher Name>/`.
- **Automated Execution**: Includes a batch script for background runs via Windows Task Scheduler.
- **Execution Summary**: Provides a color-coded report of successes and errors.

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

### Manual Execution
Run the main script:
```bash
python main.py
```

### Automated Execution (Background)
Double-click `run_auto.bat`. This script uses the configured Python environment to run the processor without user intervention.

### Configuration
- **Input Directory**: Place your raw EPUB files in `input/`.
- **Output Directory**: Processed files will appear in `finish/`.

## Project Structure

See [docs/CODEMAPS/INDEX.md](docs/CODEMAPS/INDEX.md) for a detailed architectural overview.

## License
Proprietary / Private Use
