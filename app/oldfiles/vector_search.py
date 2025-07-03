from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema.document import Document
import os

CHROMA_PATH = "app/vectorstore/chromadb"
EMBED_MODEL = "all-MiniLM-L6-v2"  # Sentence-transformers model

def get_chroma():
    """
    Returns the Chroma vector store connected to local persistence.
    """
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )

def store_chunks(chat_id, chunks: list[str], metadata: dict = None):
    """
    Stores a list of text chunks into ChromaDB with optional metadata.

    Args:
        chat_id: str, the unique chat session ID for filtering
        chunks: List of text strings to embed and store
        metadata: Dict to tag all documents (e.g., {"source": "filename.pdf"})
    """
    db = get_chroma()
    # Add chat_id to each doc's metadata
    docs = [
        Document(page_content=chunk, metadata={"chat_id": chat_id, **(metadata or {})})
        for chunk in chunks
    ]
    db.add_documents(docs)

def get_query_chunks(chat_id, query: str, top_k: int = 4) -> list[Document]:
    """
    Searches Chroma for the most relevant chunks based on the query,
    filtered by chat_id to isolate sessions.

    Args:
        chat_id: str, the unique chat session ID for filtering
        query: Natural language question or prompt
        top_k: Number of top documents to retrieve

    Returns:
        List of relevant Document objects (not strings)
    """
    db = get_chroma()
    results = db.similarity_search(query, k=top_k, filter={"chat_id": chat_id})
    
    # Return Document objects as expected by load_qa_with_sources_chain
    return results