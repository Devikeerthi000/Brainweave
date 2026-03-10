import re

def split_into_sections(text, chunk_size=2500, overlap=200):
    """
    Split text into chunks intelligently at sentence/paragraph boundaries.
    Uses overlap to preserve context between chunks.
    """
    # First try to split by paragraphs (double newlines)
    paragraphs = re.split(r'\n\n+', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If adding this paragraph exceeds limit, save current and start new
        if len(current_chunk) + len(para) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # If we got no chunks (no paragraph breaks), fall back to sentence splitting
    if len(chunks) <= 1 and len(text) > chunk_size:
        chunks = _split_by_sentences(text, chunk_size)
    
    return chunks


def _split_by_sentences(text, chunk_size=2500):
    """
    Fallback: split by sentences when no paragraph structure exists.
    """
    # Split on sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def get_document_overview(chunks, max_chars=8000):
    """
    Create a balanced overview by sampling from all parts of the document.
    """
    if not chunks:
        return ""
    
    total_chunks = len(chunks)
    
    if total_chunks == 1:
        return chunks[0][:max_chars]
    
    # Calculate how much to take from each chunk
    chars_per_chunk = max_chars // total_chunks
    
    overview_parts = []
    for i, chunk in enumerate(chunks):
        # Take beginning of first chunk, middle of middle chunks, end of last chunk
        if i == 0:
            part = chunk[:chars_per_chunk]
        elif i == total_chunks - 1:
            part = chunk[-chars_per_chunk:] if len(chunk) > chars_per_chunk else chunk
        else:
            # Take from middle
            start = max(0, len(chunk)//2 - chars_per_chunk//2)
            part = chunk[start:start + chars_per_chunk]
        
        overview_parts.append(part.strip())
    
    return "\n\n---\n\n".join(overview_parts)