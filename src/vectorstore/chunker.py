"""
Chunker Module
-------------------
Splits raw text into token-based chunks using OpenAI-compatible tokenization (via tiktoken).
Useful for preparing documents for vector embedding and retrieval pipelines.

Clarification for those worried about exposure to public API, 
this just mimics the openAI tokenizer locally. 
No API calls are made.

Author: Pete Johansson
"""

import tiktoken
from typing import List

def chunk_text(
    text: str,
    model_name: str = "gpt-3.5-turbo",
    max_tokens: int = 512,
    overlap_tokens: int = 100   
    ) -> List[str]:

    """
    Splits input text into chunks based on token count using a sliding window approach.

    Args:
        text (str): The raw text to be chunked.
        model_name (str): The name of the model to use for tokenization (used by tiktoken).
        max_tokens (int): Max tokens per chunk (e.g., 512, 1024).
        overlap_tokens (int): Tokens to overlap between chunks for 
        context continuity. - refrences on web state academic overlap is best 100-150

    Returns:
        List[str]: A list of string chunks (ready to be embedded or indexed).
    """


    # Load tokenizer for the model (can be gpt-3.5-turbo, gpt-4, etc.)
    tokenizer = tiktoken.encoding_for_model(model_name)

    # Tokenize the full input text
    tokens = tokenizer.encode(text)

    chunks = []
    start = 0
    total_tokens = len(tokens)

    # Loop with sliding window logic
    while start < total_tokens:
        end = min(start + max_tokens, total_tokens)
        chunk_tokens = tokens[start:end]

        # Decode back into text
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

        # Slide window forward with overlap
        start += max_tokens - overlap_tokens

    return chunks

