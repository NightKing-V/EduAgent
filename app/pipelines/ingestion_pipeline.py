# app/pipelines/ingestion_pipeline.py
import os
from typing import Dict, List
from dataclasses import dataclass
from tools.pdf_chunk_loader import extract_and_chunk_pdf
from services.text_processor import TextProcessorService
from services.vector_store_service import VectorStoreService, create_vector_store_service

@dataclass
class IngestionResult:
    """Data class for ingestion pipeline results"""
    summary: str
    topics: str
    chunk_count: int

class IngestionPipeline:
    """
    Ingestion pipeline with dependency injection for better testability and flexibility.
    Follows Single Responsibility and Dependency Inversion principles.
    """
    
    def __init__(self, 
                 text_processor: TextProcessorService,
                 vector_store_service: VectorStoreService):
        self.text_processor = text_processor
        self.vector_store_service = vector_store_service
    
    def process_document(self, file_path: str, chat_id: str) -> IngestionResult:
        """
        Process a document through the complete ingestion pipeline.
        
        Args:
            file_path: Path to the PDF file
            chat_id: Unique identifier for the chat session
            
        Returns:
            IngestionResult containing summary, topics, and chunk count
        """
        # Extract and chunk the PDF
        chunks = extract_and_chunk_pdf(file_path)
        
        # Process text for summary and topics
        summary = self.text_processor.summarize_text(chunks)
        topics = self.text_processor.extract_topics(chunks)
        
        # Store chunks in vector database
        metadata = {"source": os.path.basename(file_path)}
        self.vector_store_service.store_chunks(chat_id, chunks, metadata)
        
        return IngestionResult(
            summary=summary,
            topics=topics,
            chunk_count=len(chunks)
        )

def create_ingestion_pipeline() -> IngestionPipeline:
    """Factory function to create a configured ingestion pipeline"""
    from services.text_processor import get_text_processor
    
    text_processor = get_text_processor()
    vector_store_service = create_vector_store_service()
    
    return IngestionPipeline(text_processor, vector_store_service)

# Backward compatibility function
def run_ingestion_pipeline(file_path: str, chat_id: str) -> Dict:
    """Legacy function for backward compatibility"""
    pipeline = create_ingestion_pipeline()
    result = pipeline.process_document(file_path, chat_id)
    
    return {
        "summary": result.summary,
        "topics": result.topics,
        "chunk_count": result.chunk_count
    }