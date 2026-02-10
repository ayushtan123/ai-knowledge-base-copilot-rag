# AI Knowledge Base & Customer Service Copilot

RAG-powered knowledge base assistant that allows users to upload internal documents and ask questions with grounded, source-backed answers.

## Features
- Document upload via UI
- Retrieval-Augmented Generation (RAG)
- Ranked sources with file name and line number
- Rate-limited LLM calls
- Local embeddings (no embedding API cost)
- Streamlit-based UI
  
<img width="1360" height="906" alt="image" src="https://github.com/user-attachments/assets/6fe24b53-ac04-4a15-ba96-b942d0bffca3" />

Demo: https://github.com/user-attachments/assets/1d4ec67c-373c-4428-8402-d54b91766a85

## Tech Stack
- Python
- Streamlit
- ChromaDB
- Sentence Transformers (local embeddings)
- Gemini 2.5 Flash (LLM)

<img width="2705" height="1514" alt="deepseek_mermaid_20260205_15ca24" src="https://github.com/user-attachments/assets/6582b7c2-8c9d-4e26-a71c-9ce18049a24d" />

## How it works
1. User uploads `.txt` documents
2. Documents are indexed into a vector database
3. User asks a question
4. Relevant document chunks are retrieved and ranked
5. Gemini generates a grounded answer with citations

<img width="7444" height="722" alt="deepseek_mermaid_20260205_1088c8" src="https://github.com/user-attachments/assets/f4356084-078d-42cb-ab95-6c3eea532a4d" />

## Notes
- API calls are throttled to respect free-tier limits
- The system avoids hallucinations by answering only from retrieved context
- This project was an assignment for internship at Pluang (Feb 2026)

venv\Scripts\activate

