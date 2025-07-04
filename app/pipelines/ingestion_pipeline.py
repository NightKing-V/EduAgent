import os
from dataclasses import dataclass
from tools.pdf_chunk_loader import extract_and_chunk_pdf
from services.text_processor import TextProcessorService
from services.vector_store_service import VectorStoreService, create_vector_store_service

@dataclass
class IngestionResult:
    summary: str
    topics: str
    chunk_count: int

class IngestionPipeline:
    
    def __init__(self, 
                 text_processor: TextProcessorService,
                 vector_store_service: VectorStoreService):
        self.text_processor = text_processor
        self.vector_store_service = vector_store_service
    
    def process_document(self, file_path: str, chat_id: str) -> IngestionResult:
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
    from services.text_processor import create_text_processor
    
    text_processor = create_text_processor()
    vector_store_service = create_vector_store_service()
    
    return IngestionPipeline(text_processor, vector_store_service)