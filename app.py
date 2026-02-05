import streamlit as st
import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from query import answer_question

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Knowledge Base Copilot",
    page_icon="🔖",
    layout="wide"
)

CHROMA_PATH = "chroma_db"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        """
        **Purpose**  
        Upload internal documents and ask questions based on them.

        **Supported Format**
        - `.txt` files only

        **Flow**
        1. Upload documents  
        2. Index documents  
        3. Ask questions  
        """
    )
    st.divider()

    uploaded_files = st.file_uploader(
        "📄 Upload text files",
        type=["txt"],
        accept_multiple_files=True
    )

    index_button = st.button("📌 Index Uploaded Documents")

# ---------------- INDEXING LOGIC ----------------
def index_uploaded_files(files):
    documents = []

    for file in files:
        content = file.read().decode("utf-8")
        lines = content.splitlines()

        for idx, line in enumerate(lines):
            if line.strip():
                documents.append(
                    Document(
                        page_content=line.strip(),
                        metadata={
                            "source": file.name,
                            "line_number": idx + 1
                        }
                    )
                )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Clear previous index
    if os.path.exists(CHROMA_PATH):
        for root, dirs, files in os.walk(CHROMA_PATH, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

# ---------------- HANDLE INDEX BUTTON ----------------
if index_button:
    if not uploaded_files:
        st.warning("Please upload at least one text file before indexing.")
    else:
        with st.spinner("Indexing uploaded documents..."):
            index_uploaded_files(uploaded_files)
        st.success("✅ Documents indexed successfully. You can now ask questions.")

# ---------------- MAIN UI ----------------
st.title("📘 AI Knowledge Base Copilot")
st.write(
    "Upload your internal documents and ask questions. "
    "Answers are generated using document retrieval with cited sources."
)

question = st.text_input(
    "🔍 Enter your question",
    placeholder="e.g. How many paid leaves are employees entitled to?"
)

if question:
    with st.spinner("Searching documents and generating answer..."):
        answer, sources = answer_question(question)

    # Answer box
    st.subheader("✅ Answer")
    st.markdown(
        f"""
        <div style="
            background-color:#f5f7fa;
            color:#222222;
            padding:16px;
            border-radius:8px;
            border-left:5px solid #4CAF50;
            font-size:16px;
            line-height:1.6;
        ">
            {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sources
    if sources:
        st.subheader("📄 Sources (Ranked)")
        for src in sources:
            st.markdown(
                f"""
                <div style="
                    background-color:#ffffff;
                    color:#222222;
                    padding:12px;
                    margin-bottom:8px;
                    border-radius:6px;
                    border:1px solid #dddddd;
                    font-size:14px;
                ">
                    {src}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No sources available for this response.")

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "This system uses vector similarity search, ranked retrieval, "
    "and controlled LLM access to provide source-backed answers."
)
