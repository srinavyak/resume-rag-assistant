import os
from dotenv import load_dotenv
from google import genai
import chromadb

from ingest import ingest_documents

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/gemini-embedding-001"


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
         config={"task_type": "RETRIEVAL_DOCUMENT"},
    )
    return result.embeddings[0].values


def build_vector_store():
    chunks = ingest_documents()

    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name="resume_docs")

    ids, embeddings, documents, metadatas = [], [], [], []

    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i + 1}/{len(chunks)} ({chunk['source']})...")
        vector = embed_text(chunk["text"])

        ids.append(f"{chunk['source']}_{chunk['chunk_index']}")
        embeddings.append(vector)
        documents.append(chunk["text"])
        metadatas.append({"source": chunk["source"], "chunk_index": chunk["chunk_index"]})

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"\nStored {len(ids)} chunks in Chroma collection 'resume_docs'.")


if __name__ == "__main__":
    build_vector_store()        