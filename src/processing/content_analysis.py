import pdfplumber
import logging
from pathlib import Path
import hashlib

def analyze_page_content(pdf_path: Path) -> dict:
    """
    Analyze PDF pages to detect text vs. image/scanned content.
    Returns dictionary with page-by-page analysis and summary counts.
    """
    content_analysis = {
        "total_pages": 0,
        "text_pages": 0,
        "image_pages": 0,
        "mixed_pages": 0,
        "page_details": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            content_analysis["total_pages"] = len(pdf.pages)

            for i, page in enumerate(pdf.pages):
                page_info = {
                    "page_number": i + 1,
                    "has_text": False,
                    "has_images": False,
                    "text_length": 0,
                    "image_count": 0
                }

                text = page.extract_text() or ""
                if text.strip():
                    page_info["has_text"] = True
                    page_info["text_length"] = len(text)

                if page.images:
                    page_info["has_images"] = True
                    page_info["image_count"] = len(page.images)

                if page_info["has_text"] and page_info["has_images"]:
                    content_analysis["mixed_pages"] += 1
                elif page_info["has_text"]:
                    content_analysis["text_pages"] += 1
                elif page_info["has_images"]:
                    content_analysis["image_pages"] += 1

                content_analysis["page_details"].append(page_info)

    except Exception as e:
        logging.error(f"Error analyzing {pdf_path.name}: {e}")

    return content_analysis


def extract_image_metadata(pdf_path: Path) -> list[dict]:
    """
    Extract metadata about embedded images.
    Returns list of image information dictionaries.
    """
    image_metadata = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if page.images:
                    for img in page.images:
                        img_info = {
                            "page_number": i + 1,
                            "x0": img["x0"],
                            "y0": img["y0"],
                            "x1": img["x1"],
                            "y1": img["y1"],
                            "width": img["width"],
                            "height": img["height"],
                            "name": img.get("name", ""),
                            "imagetype": img.get("imagetype", "")
                        }
                        image_metadata.append(img_info)
    except Exception as e:
        logging.error(f"Error extracting image metadata from {pdf_path.name}: {e}")

    return image_metadata


def extract_text_by_page(pdf_path: Path) -> list[dict]:
    """
    Extract text with page numbers and metadata per page.
    Useful for fine-grained vectorization.
    """
    pages_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                pages_text.append({
                    "page_number": i + 1,
                    "text": text,
                    "word_count": len(text.split()),
                    "has_images": len(page.images) > 0
                })
    except Exception as e:
        logging.error(f"Error extracting text by page from {pdf_path.name}: {e}")

    return pages_text


def generate_content_hash(text: str) -> str:
    """
    Generate an MD5 hash from input text for integrity tracking.
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()
