import os
from pathlib import Path
from pypdf import PdfReader

DOCS_DIR = Path("documents")
CHUNK_SIZE = 800       # target characters per chunk
CHUNK_OVERLAP = 150    # characters shared between consecutive chunks


def load_text_from_file(filepath: Path) -> str:
    """Extract raw text from a PDF or .txt file."""
    if filepath.suffix.lower() == ".pdf":
        reader = PdfReader(str(filepath))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif filepath.suffix.lower() == ".txt":
        return filepath.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {filepath.suffix}")


def split_into_paragraphs(text: str) -> list[str]:
    """First pass: split on blank lines (paragraph boundaries)."""
    raw_paragraphs = text.split("\n\n")
    return [p.strip() for p in raw_paragraphs if p.strip()]


def chunk_text(paragraphs: list[str], chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list[str]:
    """
    Structure-aware chunking with overlap:
    - Combine paragraphs until adding another would exceed chunk_size.
    - Start the next chunk by re-including the tail of the previous one (the overlap).
    """
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 1 <= chunk_size:
            current += ("\n" if current else "") + para
            print(current,"line39")
        else:
            if current:
                chunks.append(current)
            # start new chunk, carrying over the tail of the previous chunk
            tail = current[-overlap:] if current else ""
            current = (tail + "\n" + para) if tail else para

    if current:
        chunks.append(current)

    return chunks


def ingest_documents():
    all_chunks = []  # list of dicts: {source, chunk_index, text}

    for filepath in DOCS_DIR.iterdir():
        if filepath.suffix.lower() not in (".pdf", ".txt"):
            continue

        print(f"Processing {filepath.name}...")
        text = load_text_from_file(filepath)
        paragraphs = split_into_paragraphs(text)
        chunks = chunk_text(paragraphs)

        for i, chunk in enumerate(chunks):
            print(i,chunk, "line66")
            all_chunks.append({
                "source": filepath.name,
                "chunk_index": i,
                "text": chunk,
            })

        print(f"  -> {len(chunks)} chunks")

    return all_chunks


if __name__ == "__main__":
    chunks = ingest_documents()
    print(f"\nTotal chunks across all documents: {len(chunks)}")
    print("\n--- Sample chunk ---")
    print(chunks[0]["source"], "| chunk", chunks[0]["chunk_index"])
    print(chunks[0]["text"][:300])