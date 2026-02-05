# AI Knowledge Base & Customer Service Copilot

This project is an AI-powered knowledge base assistant that allows users to upload internal documents and ask questions with grounded, source-backed answers.

## Features
- Document upload via UI
- Retrieval-Augmented Generation (RAG)
- Ranked sources with file name and line number
- Rate-limited LLM calls
- Local embeddings (no embedding API cost)
- Streamlit-based UI

## Tech Stack
- Python
- Streamlit
- ChromaDB
- Sentence Transformers (local embeddings)
- Gemini 2.5 Flash (LLM)

## How it works
1. User uploads `.txt` documents
2. Documents are indexed into a vector database
3. User asks a question
4. Relevant document chunks are retrieved and ranked
5. Gemini generates a grounded answer with citations

## Notes
- API calls are throttled to respect free-tier limits
- The system avoids hallucinations by answering only from retrieved context
