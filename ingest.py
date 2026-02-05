import os
import sys
import platform

# Fix for Windows: pwd module is Unix-only, provide a dummy module
if platform.system() == "Windows":
    import types
    sys.modules['pwd'] = types.ModuleType('pwd')


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

DATA_PATH = "data"
CHROMA_PATH = "chroma_db"

def ingest_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            file_path = os.path.join(DATA_PATH, file)

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines):
                if line.strip():
                    documents.append(
                        Document(
                            page_content=line.strip(),
                            metadata={
                                "source": file,
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

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print("Documents indexed with source + line numbers.")

if __name__ == "__main__":
    ingest_documents()