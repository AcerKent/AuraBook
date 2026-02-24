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
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to the output directory for processed files."
    )
    args = parser.parse_args()

    input_dir = Path(args.input) if args.input else None
    output_dir = Path(args.output) if args.output else None
    process_workflow(input_dir=input_dir, output_dir=output_dir)
