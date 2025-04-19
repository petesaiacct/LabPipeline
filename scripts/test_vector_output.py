# scripts/test_vector_output.py

"""
Test script to process one document:
- Chunk the text
- Generate embeddings
- Save as JSON for inspection
"""

import sys
from pathlib import Path

# ✅ Add project root to Python path BEFORE imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from src.vectorstore.chunker import chunk_text
from src.vectorstore.vector_doc_builder import create_vector_documents_from_metadata

# === Configurable Parameters ===
INPUT_TXT = "data/processed/papers/text/2019_Whissel_CCK_GABA_neurons.txt"
OUTPUT_JSON = "data/debug/vectors_2019_Whissel_CCK_GABA_neurons.json"
EMBED_MODEL = "all-MiniLM-L6-v2"
DOC_METADATA = {
    "doc_id": "2019_Whissel_CCK_GABA_neurons",
    "title": "Selective Activation of Cholecystokinin-Expressing GABA (CCK-GABA) Neurons",
    "source": "internal_report"
}
CHUNK_PARAMS = {
    "model_name": "gpt-3.5-turbo",
    "max_tokens": 512,
    "overlap_tokens": 100
}

# === Create Output Directory ===
Path("data/debug").mkdir(parents=True, exist_ok=True)

# === Load Input Text ===
with open(INPUT_TXT, "r", encoding="utf-8") as f:
    raw_text = f.read()

# === Generate Vector Chunks ===
chunks = create_vector_documents_from_metadata(
    metadata=DOC_METADATA,
    raw_text=raw_text,
    chunk_fn=lambda txt: chunk_text(txt, **CHUNK_PARAMS),
    embedding_model_name=EMBED_MODEL
)

# === Save to JSON ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as out_file:
    json.dump(chunks, out_file, indent=2)

print(f"✅ Saved {len(chunks)} vector documents to {OUTPUT_JSON}")

