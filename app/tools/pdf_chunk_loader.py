from abc import ABC, abstractmethod
from typing import List, Optional
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from dataclasses import dataclass

@dataclass
class ChunkingConfig:
    """Configuration for text chunking"""
    chunk_size: int = 800
    chunk_overlap: int = 100
    separators: Optional[List[str]] = None

class DocumentProcessor(ABC):
    """Abstract base class for document processing (Strategy Pattern)"""
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass

class PDFProcessor(DocumentProcessor):
    """Concrete implementation for PDF processing"""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        with open(file_path, "rb") as f:
            doc = fitz.open(stream=f.read(), filetype="pdf")
            full_text = "\n\n".join([page.get_text() for page in doc])
        return full_text

class TextChunker:
    """Handles text chunking with configurable parameters"""
    
    def __init__(self, config: ChunkingConfig):
        self.config = config
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators
        )
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        return self.splitter.split_text(text)

class DocumentChunkingService:
    """Service that orchestrates document processing and chunking"""
    
    def __init__(self, processor: DocumentProcessor, chunker: TextChunker):
        self.processor = processor
        self.chunker = chunker
    
    def extract_and_chunk(self, file_path: str) -> List[str]:
        """Extract text from document and chunk it"""
        text = self.processor.extract_text(file_path)
        return self.chunker.chunk_text(text)

# Factory functions
def create_pdf_chunking_service(config: Optional[ChunkingConfig] = None) -> DocumentChunkingService:
    """Create a PDF chunking service with default configuration"""
    chunking_config = config or ChunkingConfig()
    processor = PDFProcessor()
    chunker = TextChunker(chunking_config)
    return DocumentChunkingService(processor, chunker)



def extract_and_chunk_pdf(path: str, chunk_size=800, chunk_overlap=100) -> List[str]:
    """Legacy function for backward compatibility"""
    config = ChunkingConfig(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    service = create_pdf_chunking_service(config)
    return service.extract_and_chunk(path)

# LangChain Tool wrapper
pdf_chunk_tool = Tool(
    name="PDFChunkLoader",
    func=extract_and_chunk_pdf,
    description="Extracts and chunks text from a research paper PDF. Input is the file path."
)