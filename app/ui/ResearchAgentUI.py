from utils.file_handler import cleanup_temp_file, save_uploaded_file_temporarily
import streamlit as st
from typing import Optional
from ui.UISessionManager import UISessionManager

class ResearchAgentUI:
    """Handles Research Agent UI interactions"""
    
    def __init__(self, session_manager: UISessionManager):
        self.session_manager = session_manager
    
    def render_upload_section(self):
        """Render the file upload section"""
        st.subheader("Upload a Research Paper (PDF)")
        uploaded_paper = st.file_uploader(
            "Choose a PDF file", 
            type=["pdf"], 
            key="research_pdf"
        )
        return uploaded_paper
    
    def process_paper_analysis(self, uploaded_paper) -> Optional[dict]:
        """Process paper analysis and return results"""
        if uploaded_paper is None:
            return None
        
        st.success("✅ Paper uploaded. Ready to summarize and chat with the agent.")
        
        if st.button("🔍 Analyze Paper"):
            try:
                # Save file temporarily
                temp_pdf_path = save_uploaded_file_temporarily(
                    uploaded_file=uploaded_paper, 
                    chat_id=self.session_manager.get_chat_id()
                )
                
                # Import and run ingestion pipeline
                from pipelines.ingestion_pipeline import create_ingestion_pipeline
                
                st.info("Running ResearchAgent... (this may take a moment)")
                
                # Use the OOP approach
                pipeline = create_ingestion_pipeline()
                result = pipeline.process_document(
                    file_path=temp_pdf_path,
                    chat_id=self.session_manager.get_chat_id()
                )
                
                # Cleanup
                cleanup_temp_file(temp_pdf_path)

                
                return result

            except Exception as e:
                st.error(f"Error analyzing paper: {str(e)}")
                return None
        
        return None
