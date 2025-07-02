from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

def get_chroma():
    return Chroma(
        persist_directory="app/vectorstore/chroma",
        embedding_function=OllamaEmbeddings(model="nomic-embed-text-v1")
    )

def store_chunks(chunks, metadata):
    db = get_chroma()
    db.add_texts(chunks, metadatas=[metadata] * len(chunks))

def query_chunks(query: str, top_k=4):
    db = get_chroma()
    docs = db.similarity_search(query, k=top_k)
    return "\n\n".join([doc.page_content for doc in docs])
