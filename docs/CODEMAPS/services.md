# Services Architecture

**Last Updated:** 2026-02-12
**Location:** `src/services/`

This document details the specialized service modules used by the Core Processor.

## Modules

### 1. EPUB Parser (`epub_parser.py`)
Responsible for extracting metadata from `.epub` files using `EbookLib`.

| Function | Purpose | Returns |
| due | ------- | ------- |
| `extract_epub_metadata(path)` | Extracts Date, Publisher, Author, Subject | `dict` |

- **Logic**:
    - **Date**: Tries `DC:date`. Parses `YYYY-MM-DD` or `YYYY-MM`.
    - **Publisher**: Reads `DC:publisher`. Used for primary categorization.
    - **Author**: Reads `DC:creator`. Used for filename appending.

### 2. PDF Converter (`converter.py`)
Wraps the `ebook-convert` command line tool from Calibre.

| Function | Purpose |
| due | ------- |
| `convert_epub_to_pdf(input_path, output_dir)` | Converts EPUB to PDF |

- **Key Features**:
    - Captures output as bytes to prevent `UnicodeDecodeError` on Windows (CP950).
    - Returns `Path` to generated PDF or `None` on failure.

### 3. Metadata Fetcher (`metadata_fetcher.py`)
External API fallback when local metadata is missing.

| Function | Purpose |
| due | ------- |
| `fetch_publication_date(query)` | Searches Open Library for publication year |

### 4. Categorizer (`categorizer.py`)
Keyword-based fallback when no Publisher metadata exists.

| Function | Purpose |
| due | ------- |
| `categorize_book(filename)` | Matches filename keywords to preset categories |

### 5. Cleaner (`cleaner.py`)
String manipulation utility.

| Function | Purpose |
| due | ------- |
| `clean_filename(name)` | Removes specific patterns (e.g., `(2023)`, `[Retail]`) |
