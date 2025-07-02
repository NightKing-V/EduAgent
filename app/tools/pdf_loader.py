import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool

def extract_and_chunk_pdf(path: str, chunk_size=800, chunk_overlap=100) -> list[str]:
    """Extracts and chunks text from a PDF file at given path."""
    with open(path, "rb") as f:
        doc = fitz.open(stream=f.read(), filetype="pdf")
        full_text = "\n\n".join([page.get_text() for page in doc])
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(full_text)

# LangChain Tool wrapper
pdf_chunk_tool = Tool(
    name="PDFChunkLoader",
    func=extract_and_chunk_pdf,
    description="Extracts and chunks text from a research paper PDF. Input is the file path."
)
