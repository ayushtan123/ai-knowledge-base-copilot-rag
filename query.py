import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from prompts import QA_PROMPT

load_dotenv()

CHROMA_PATH = "chroma_db"

COOLDOWN_SECONDS = 60   # 1 Gemini call per minute
LAST_CALL_TIME = 0


def answer_question(question: str):
    global LAST_CALL_TIME

    now = time.time()
    if now - LAST_CALL_TIME < COOLDOWN_SECONDS:
        wait = int(COOLDOWN_SECONDS - (now - LAST_CALL_TIME))
        return f"Please wait {wait} seconds before asking another question.", []

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    # Returns (Document, score) tuples
    docs_with_scores = vector_store.similarity_search_with_score(question, k=4)

    if not docs_with_scores:
        return "I could not find this information in the available documents.", []

    context = ""
    sources = []

    # Use top 2–3 chunks only
    for rank, (doc, score) in enumerate(docs_with_scores[:3], start=1):
        context += doc.page_content + "\n"

        file_name = doc.metadata.get("source", "Unknown file")
        line_no = doc.metadata.get("line_number", "N/A")

        sources.append(
            f"#{rank} {file_name} (line {line_no}) — relevance: {round(score, 4)}"
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_retries=0
    )

    prompt = QA_PROMPT.format(
        context=context[:2000],   # token cap
        question=question
    )

    try:
        response = llm.invoke(prompt)
        LAST_CALL_TIME = time.time()
        return response.content, sources

    except Exception:
        LAST_CALL_TIME = time.time()
        return (
            "The AI service is currently rate-limited. "
            "This system uses controlled API usage with throttling and caching. "
            "Please try again later.",
            []
        )
