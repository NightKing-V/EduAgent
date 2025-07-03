# core/interfaces.py - Abstract interfaces/contracts

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain.schema.document import Document

class VectorSearchInterface(ABC):
    """
    Abstract interface for vector search operations.
    
    This defines the CONTRACT - what methods any vector search implementation
    must provide, without specifying HOW they work.
    
    Benefits:
    - Other classes can depend on this interface, not concrete implementations
    - We can swap ChromaDB for Pinecone/Weaviate without changing other code
    - Easy to mock for testing
    - Clear documentation of what the service provides
    """
    
    @abstractmethod
    def store_chunks(self, chat_id: str, chunks: List[str], metadata: Dict = None) -> None:
        """
        Store text chunks in vector database.
        
        Args:
            chat_id: Unique identifier for the chat session
            chunks: List of text chunks to store
            metadata: Optional metadata to attach to chunks
        """
        pass
    
    @abstractmethod
    def get_query_chunks(self, chat_id: str, query: str, top_k: int = 4) -> List[Document]:
        """
        Retrieve relevant chunks for a given query.
        
        Args:
            chat_id: Unique identifier for the chat session
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of Document objects containing relevant chunks
        """
        pass


class ResearchServiceInterface(ABC):
    """
    Abstract interface for research operations.
    
    This defines what any research service must provide.
    """
    
    @abstractmethod
    def answer_question(self, question: str, chat_id: str) -> str:
        """
        Answer a research question using available documents.
        
        Args:
            question: The research question to answer
            chat_id: Unique identifier for the chat session
            
        Returns:
            Answer string based on available documents
        """
        pass


class DocumentProcessorInterface(ABC):
    """
    Abstract interface for document processing operations.
    """
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract text from a document file."""
        pass
    
    @abstractmethod
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks for vector storage."""
        pass
    
    @abstractmethod
    def summarize_document(self, text: str) -> str:
        """Generate a summary of the document."""
        pass


# Example of how interfaces enable polymorphism
class LLMInterface(ABC):
    """Interface for different LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass

# Different implementations can be swapped easily:
# - OpenAILLM(LLMInterface)
# - MistralLLM(LLMInterface) 
# - ClaudeLLM(LLMInterface)
# - LocalLLM(LLMInterface)