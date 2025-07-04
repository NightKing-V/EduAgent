# app/services/vector_store_service.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema.document import Document

class VectorStoreInterface(ABC):
    """Interface for vector store operations (Interface Segregation)"""
    
    @abstractmethod
    def store_documents(self, documents: List[Document]) -> None:
        pass
    
    @abstractmethod
    def search_similar(self, query: str, k: int = 4, filter_dict: Optional[Dict] = None) -> List[Document]:
        pass

class ChromaVectorStore(VectorStoreInterface):
    """Concrete implementation using ChromaDB"""
    
    def __init__(self, persist_directory: str, embedding_model: str = "all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model)
        self._db = None
    
    @property
    def db(self):
        """Lazy initialization of ChromaDB"""
        if self._db is None:
            self._db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        return self._db
    
    def store_documents(self, documents: List[Document]) -> None:
        """Store documents in the vector store"""
        self.db.add_documents(documents)
    
    def search_similar(self, query: str, k: int = 4, filter_dict: Optional[Dict] = None) -> List[Document]:
        """Search for similar documents"""
        return self.db.similarity_search(query, k=k, filter=filter_dict)

class VectorStoreService:
    """Service class that handles vector store operations with dependency injection"""
    
    def __init__(self, vector_store: VectorStoreInterface):
        self.vector_store = vector_store
    
    def store_chunks(self, chat_id: str, chunks: List[str], metadata: Optional[Dict] = None) -> None:
        """Store text chunks as documents"""
        documents = [
            Document(
                page_content=chunk,
                metadata={"chat_id": chat_id, **(metadata or {})}
            )
            for chunk in chunks
        ]
        self.vector_store.store_documents(documents)
    
    def get_query_chunks(self, chat_id: str, query: str, top_k: int = 4) -> List[Document]:
        """Search for relevant chunks filtered by chat_id"""
        return self.vector_store.search_similar(
            query=query,
            k=top_k,
            filter_dict={"chat_id": chat_id}
        )

# Factory function for creating the service
def create_vector_store_service(persist_directory: str = "app/vectorstore/chromadb") -> VectorStoreService:
    """Create a vector store service with ChromaDB backend"""
    chroma_store = ChromaVectorStore(persist_directory)
    return VectorStoreService(chroma_store)
