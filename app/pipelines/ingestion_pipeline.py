from app.tools.pdf_chunk_loader import extract_and_chunk_pdf
from app.tools.summarizer import summarize_text
from app.tools.topic_extractor import extract_topics
from app.tools.vector_search import store_chunks, query_chunks

def run_ingestion_pipeline(file_path: str, chat_id: str):
    chunks = extract_and_chunk_pdf(file_path)

    summary = summarize_text(chunks)

    topics = extract_topics(chunks)

    store_chunks(chat_id=chat_id, chunks=chunks, metadata={"source": os.path.basename(file_path)})

    return {
        "summary": summary,
        "topics": topics,
        "chunk_count": len(chunks)
    }
