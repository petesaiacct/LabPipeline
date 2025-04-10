from dataclasses import dataclass

@dataclass
class ProcessingConfig:
    extract_text: bool = True
    extract_metadata: bool = True
    extract_title: bool = True
    analyze_content: bool = True
    extract_images: bool = True
    extract_text_by_page: bool = True
    generate_hash: bool = True
