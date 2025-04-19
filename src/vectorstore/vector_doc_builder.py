# src/vectorstore/vector_doc_builder.py

"""
Vector Document Builder
-----------------------
Splits documents into chunks and generates embeddings using sentence-transformers.
Prepares data for insertion into a vector database (e.g., Chroma, FAISS).

Author: Pete Johansson
"""

from sentence_transformers import SentenceTransformer
from datetime import datetime
from typing import List, Dict, Callable
import uuid

def create_vector_documents_from_metadata(
    metadata: Dict,
    raw_text: str,
    chunk_fn: Callable[[str], List[str]],
    embedding_model_name: str = "all-MiniLM-L6-v2"
) -> List[Dict]:
    """
    Generates a list of chunk-level vector documents with embeddings and metadata.

    Args:
        metadata (Dict): Metadata about the source document (e.g., doc_id, title, source).
        raw_text (str): The full text of the document.
        chunk_fn (Callable): A function that takes text and returns a list of chunked strings.
        embedding_model_name (str): HuggingFace name of the embedding model.

    Returns:
        List[Dict]: List of documents with text, embedding, and metadata for vector DB insertion.
    """
    
    # Load embedding model
    model = SentenceTransformer(embedding_model_name)

    # Chunk the text
    chunks = chunk_fn(raw_text)

    # Embed each chunk
    embeddings = model.encode(chunks, convert_to_numpy=True)

    # Assemble final vector documents
    vector_docs = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_doc = {
            "id": str(uuid.uuid4()),
            "text": chunk,
            "embedding": embedding.tolist(),  # Some VDBs like Chroma prefer list not np.array
            "metadata": {
                "doc_id": metadata.get("doc_id", "unknown"),
                "title": metadata.get("title", "Untitled"),
                "source": metadata.get("source", "unknown"),
                "page_num": metadata.get("page_num", None),  # Optional
                "chunk_index": i,
                "token_count": len(chunk.split()),  # Approximate; true token count requires tokenizer
                "embedding_model": embedding_model_name,
                "timestamp": datetime.now().isoformat()
            }
        }
        vector_docs.append(vector_doc)

    return vector_docs
