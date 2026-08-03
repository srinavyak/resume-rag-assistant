# Resume RAG Assistant

A retrieval-augmented generation (RAG) tool that answers questions grounded in
resume and project documents, instead of relying on an LLM's raw training data.

## How it works
1. Documents (PDF/TXT) are chunked using structure-aware splitting with overlap.
2. Chunks are embedded using Gemini's embedding model and stored in Chroma.
3. Incoming questions are embedded the same way and matched against stored chunks
   via similarity search.
4. Retrieved chunks are passed to Gemini as grounding context to generate an answer,
   with a distance-threshold guardrail to avoid answering when there's no good match.

## Stack
Python, Google Gemini API (generation + embeddings), ChromaDB, Streamlit

## Evaluation
Includes a golden-dataset evaluation harness (`eval.py`) with both positive test
cases (verifying correct answers) and a negative test case (verifying the system
correctly refuses to answer out-of-scope questions rather than hallucinating).

## Live demo
[link once deployed]