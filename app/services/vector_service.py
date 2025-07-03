# services/vector_service.py - Implementation of vector operations
from typing import List, Dict
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.document import Document

from core.interfaces import VectorSearchInterface

class VectorService(VectorSearchInterface):
    def __init__(self, chroma_path: str = "app/vectorstore/chromadb", 
                 embed_model: str = "all-MiniLM-L6-v2"):
        self.chroma_path = chroma_path
        self.embed_model = embed_model
        self._db = None
    
    def _get_chroma(self):
        """Lazy initialization of Chroma DB"""
        if self._db is None:
            embedding = HuggingFaceEmbeddings(model_name=self.embed_model)
            self._db = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=embedding
            )
        return self._db
    
    def store_chunks(self, chat_id: str, chunks: List[str], metadata: Dict = None) -> None:
        """Store chunks in vector database"""
        db = self._get_chroma()
        docs = [
            Document(
                page_content=chunk, 
                metadata={"chat_id": chat_id, **(metadata or {})}
            )
            for chunk in chunks
        ]
        db.add_documents(docs)
    
    def get_query_chunks(self, chat_id: str, query: str, top_k: int = 4) -> List[Document]:
        """Retrieve relevant chunks for a query"""
        db = self._get_chroma()
        results = db.similarity_search(
            query, 
            k=top_k, 
            filter={"chat_id": chat_id}
        )
        return results