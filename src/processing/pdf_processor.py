# pdf_processor.py — Extract Text and Metadata from PDFs

import os
import re
import json
import pdfplumber # Ensure this is in requirements.txt
from pathlib import Path
import logging # Consider using logging instead of print for better control
from src.config.processing_config import ProcessingConfig
from src.processing.content_analysis import (
    analyze_page_content,
    extract_image_metadata,
    extract_text_by_page,
    generate_content_hash
)


# --- Configuration ---
# Define input and output paths using pathlib for OS-independent access
# Assumes script is run from the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent # Get project root assuming src/processing/pdf_processor.py
# Alternatively, if running from root is guaranteed: BASE_DIR = Path(".")
RAW_PDF_DIR = BASE_DIR / "data/raw/papers"
TEXT_OUTPUT_DIR = BASE_DIR / "data/processed/papers/text"
META_OUTPUT_DIR = BASE_DIR / "data/processed/papers/metadata"

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Core Functions ---

def extract_pdf_text(pdf_path: Path) -> str | None:
    """
    Extract all text from a PDF file using pdfplumber, page by page.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        str | None: Joined string of all pages' text, or None if an error occurs.
    """
    full_text = []
    logging.info(f"Attempting to read {pdf_path.name}...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                logging.warning(f"No pages found in {pdf_path.name}")
                return "" # Return empty string for empty PDFs

            for i, page in enumerate(pdf.pages):
                # Extract text from each page (or empty string if None)
                # Add basic progress logging per page if needed for long docs
                # logging.debug(f"Extracting text from page {i+1}/{len(pdf.pages)} of {pdf_path.name}")
                text = page.extract_text() or ""
                full_text.append(text)
        
        logging.info(f"Successfully extracted text from {pdf_path.name}")
        return "\n".join(full_text)
    # Consider catching more specific pdfplumber exceptions if needed
    except Exception as e:
        logging.error(f"Error reading {pdf_path.name}: {e}", exc_info=True) # Log traceback
        return None

def extract_metadata_from_filename(filename: str) -> dict:
    """
    Extract year, first author, and keyword from the filename using regex.
    Expected format: [YYYY]_Author_Keyword.pdf (or similar based on final convention)

    Args:
        filename (str): The filename (e.g., "[2017]_Vaswani_Attention.pdf").

    Returns:
        dict: Dictionary containing 'year', 'author', 'keyword'. Values are None if match fails.
    """
    # Regex pattern based on the convention: [YYYY]_Author_Keyword(s).pdf
    # This version allows Author and Keyword to contain more than just \w (e.g., hyphens)
    # It captures everything after the second underscore as the keyword part.
    pattern = r"(\d{4})_([^_]+)_(.+)\.pdf" 
    match = re.match(pattern, filename)
    
    metadata = {
        "year": None,
        "author": None,
        "keyword_string": None # Changed name for clarity
    }
    
    if match:
        year, author, keyword_string = match.groups()
        metadata.update({
            "year": int(year), # Convert year to integer
            "author": author,
            "keyword_string": keyword_string
        })
        logging.debug(f"Extracted metadata from filename '{filename}': {metadata}")
    else:
        logging.warning(f"Could not extract metadata from filename: '{filename}'. Does it match the expected pattern '[YYYY]_Author_Keyword(s).pdf'?")
        
    return metadata

def extract_title_heuristic(text: str, num_lines: int = 5) -> str | None:
    """
    Attempt to extract a title from the first few non-empty lines of text.
    This is a simple heuristic and may not always be accurate.

    Args:
        text (str): The full extracted text from the PDF.
        num_lines (int): How many non-empty lines to check for a potential title.

    Returns:
        str | None: The potential title string, or None if no suitable line found.
    """
    if not text:
        return None
        
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    
    potential_title = None
    if lines:
        # Often titles are short and in the first few lines.
        # This heuristic checks the first `num_lines` non-empty lines.
        for i in range(min(num_lines, len(lines))):
             # Simple check: assume title is relatively short and doesn't look like abstract/body
             if len(lines[i]) < 150 and len(lines[i]) > 5: # Avoid grabbing very short/long lines
                 potential_title = lines[i]
                 break # Take the first plausible line

    logging.debug(f"Heuristic extracted title: '{potential_title}'")
    return potential_title


def process_pdfs(config: ProcessingConfig = ProcessingConfig()):
    """
    Process all PDF files in the raw papers directory:
    - Extract text
    - Save text to /data/processed/papers/text/
    - Extract metadata (from filename and text heuristic)
    - Save metadata as JSON to /data/processed/papers/metadata/
    """
    logging.info(f"Starting PDF processing in directory: {RAW_PDF_DIR}")
    processed_count = 0
    error_count = 0

    # Ensure output directories exist (redundant if main() ensures, but safe)
    TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    META_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        logging.warning(f"No PDF files found in {RAW_PDF_DIR}. Exiting.")
        return

    logging.info(f"Found {len(pdf_files)} PDF files to process.")

    for pdf_file in pdf_files:
        logging.info(f"--- Processing {pdf_file.name} ---")

        # Configurable processing pipeline — toggle steps in ProcessingConfig

        metadata = {}

        # 1. Extract text
        text = None
        if config.extract_text:
            text = extract_pdf_text(pdf_file)
            if text is None:
                logging.warning(f"Skipping {pdf_file.name} due to text extraction error.")
                error_count += 1
                continue
            text_filename = TEXT_OUTPUT_DIR / f"{pdf_file.stem}.txt"
            text_filename.write_text(text, encoding="utf-8")
            metadata["processed_text_path"] = str(text_filename.resolve())

        # 2. Metadata from filename
        if config.extract_metadata:
            metadata.update(extract_metadata_from_filename(pdf_file.name))

        # 3. Title heuristic
        if config.extract_title and text:
            metadata["extracted_title_heuristic"] = extract_title_heuristic(text)

        # 4. Page-level content analysis
        if config.analyze_content:
            metadata["content_analysis"] = analyze_page_content(pdf_file)

        # 5. Extract image metadata
        if config.extract_images:
            metadata["image_metadata"] = extract_image_metadata(pdf_file)
            metadata["has_scanned_content"] = metadata["content_analysis"]["image_pages"] > 0

        # 6. Text by page (for vector chunking)
        if config.extract_text_by_page:
            metadata["pagewise_text"] = extract_text_by_page(pdf_file)

        # 7. Optional content hash
        if config.generate_hash and text:
            metadata["content_hash"] = generate_content_hash(text)

        # 8. Save final metadata
        meta_filename = META_OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(meta_filename, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logging.info(f"--- Finished processing {pdf_file.name} ---")
        processed_count += 1



    logging.info(f"\n--- Processing Summary ---")
    logging.info(f"Total PDFs Found: {len(pdf_files)}")
    logging.info(f"Successfully Processed: {processed_count}")
    logging.info(f"Errors Encountered: {error_count}")
    logging.info(f"--------------------------")


def main():
    config = ProcessingConfig(
        extract_text=True,
        extract_metadata=True,
        extract_title=True,
        analyze_content=True,
        extract_images=True,
        extract_text_by_page=True,
        generate_hash=True
    )
    process_pdfs(config)

if __name__ == "__main__":
    main()




