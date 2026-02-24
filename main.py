import argparse
from pathlib import Path
from src.core.processor import process_workflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AuraBook - Ebook Archiver")
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to the input directory containing EPUB files."
    )
    args = parser.parse_args()

    input_dir = Path(args.input) if args.input else None
    process_workflow(input_dir=input_dir)
