import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/gemini-embedding-001"
GENERATION_MODEL = "models/gemini-flash-latest"

TOP_K = 4                    # how many chunks to retrieve
DISTANCE_THRESHOLD = 1.1 # tune this empirically — see note below

chroma_client = chromadb.PersistentClient(path="chroma_db")
try:
    collection = chroma_client.get_collection(name="resume_docs")
except Exception:
    print("Collection not found — building vector store from documents/...")
    from embed_and_store import build_vector_store
    build_vector_store()
    collection = chroma_client.get_collection(name="resume_docs")


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(model=EMBEDDING_MODEL, contents=text,config={"task_type": "RETRIEVAL_QUERY"},)
    return result.embeddings[0].values


def retrieve_chunks(question: str):
    query_vector = embed_text(question)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=TOP_K,
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("DEBUG distances:", distances)          # <-- add this
    for doc, meta, dist in zip(docs, metadatas, distances):
        print(f"  {meta['source']} (dist={dist:.3f}): {doc[:80]}...")  # <-- and this

    return list(zip(docs, metadatas, distances))


def build_prompt(question: str, retrieved) -> str:
    context_blocks = []
    for doc, meta, _ in retrieved:
        context_blocks.append(f"[Source: {meta['source']}]\n{doc}")
    context = "\n\n---\n\n".join(context_blocks)

    return f"""Answer the question using ONLY the context below. If the context doesn't
contain enough information to answer, say "I don't have enough information to answer
that" instead of guessing.

Context:
{context}

Question: {question}

Answer:"""


def answer_question(question: str):
    retrieved = retrieve_chunks(question)

    # Guardrail: if even the best match is too dissimilar, don't bother calling the LLM
    best_distance = min(d for _, _, d in retrieved)
    if best_distance > DISTANCE_THRESHOLD:
        return "I don't have enough information to answer that.", []

    prompt = build_prompt(question, retrieved)
    response = client.models.generate_content(model=GENERATION_MODEL, contents=prompt)

    sources = sorted(set(meta["source"] for _, meta, _ in retrieved))
    return response.text, sources


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or 'quit'): ")
        if question.lower() == "quit":
            break

        answer, sources = answer_question(question)
        print(f"\nAnswer: {answer}")
        if sources:
            print(f"Sources: {', '.join(sources)}")