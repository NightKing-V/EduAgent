# app/main.py - Updated with OOP principles and proper error handling
import streamlit as st
import os
import sys
from typing import Optional

# 📌 Make sure Python can find other app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.uuid_gen import generate_uuid
from utils.file_handler import cleanup_temp_file, save_uploaded_file_temporarily

class UISessionManager:
    """Manages UI session state and initialization"""
    
    def __init__(self):
        self.chat_id = self._initialize_chat_id()
    
    def _initialize_chat_id(self) -> str:
        """Initialize chat ID only once per session"""
        if "chat_id" not in st.session_state:
            st.session_state.chat_id = generate_uuid()
        return st.session_state.chat_id
    
    def get_chat_id(self) -> str:
        """Get current chat ID"""
        return self.chat_id

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
                
                # Display results
                self._display_analysis_results(result)
                
                return {
                    "summary": result.summary,
                    "topics": result.topics,
                    "chunk_count": result.chunk_count
                }
                
            except Exception as e:
                st.error(f"Error analyzing paper: {str(e)}")
                return None
        
        return None
    
    def _display_analysis_results(self, result):
        """Display analysis results in the UI"""
        st.markdown("### Paper Summary")
        st.write(result.summary)
        
        st.markdown("### Extracted Topics")
        st.write(result.topics)
        
        st.markdown("### Processing Info")
        st.info(f"Processed {result.chunk_count} text chunks")
    
    def handle_question_answering(self):
        """Handle the Q&A interaction"""
        question = st.text_input("Ask a question about the research paper:")
        
        if st.button("Ask ResearchAgent") and question.strip():
            try:
                from agents.research_agent import create_research_agent_service
                
                with st.spinner("ResearchAgent is thinking..."):
                    # Use the OOP service
                    service = create_research_agent_service()
                    answer = service.ask_question(
                        question=question,
                        chat_id=self.session_manager.get_chat_id()
                    )
                    
                    st.markdown("### Answer:")
                    st.write(answer)
                    
            except Exception as e:
                st.error(f"Error running ResearchAgent: {str(e)}")

class ExamAgentUI:
    """Handles Exam Agent UI interactions"""
    
    def __init__(self, session_manager: UISessionManager):
        self.session_manager = session_manager
    
    def render_upload_section(self):
        """Render the file upload section for exam agent"""
        st.subheader("Upload Exam Paper and Study Materials")
        
        uploaded_exam = st.file_uploader(
            "Upload exam paper (PDF or TXT)", 
            type=["pdf", "txt"], 
            key="exam_pdf"
        )
        
        uploaded_notes = st.file_uploader(
            "Upload study material (PDF or TXT)", 
            type=["pdf", "txt"], 
            accept_multiple_files=True, 
            key="study_materials"
        )
        
        return uploaded_exam, uploaded_notes
    
    def process_exam_analysis(self, uploaded_exam, uploaded_notes):
        """Process exam analysis"""
        if uploaded_exam is None or not uploaded_notes:
            return
        
        st.success("✅ Exam and materials uploaded.")
        
        if st.button("🧠 Analyze Exam & Match Study Areas"):
            try:
                # Save files temporarily
                exam_path = save_uploaded_file_temporarily(
                    uploaded_file=uploaded_exam,
                    chat_id=self.session_manager.get_chat_id()
                )
                
                study_paths = []
                for note in uploaded_notes:
                    note_path = save_uploaded_file_temporarily(
                        uploaded_file=note,
                        chat_id=self.session_manager.get_chat_id()
                    )
                    study_paths.append(note_path)
                
                # Import and run exam analysis
                from agents.exam_agent import create_exam_agent_service
                
                st.info("Running ExamAgent... (this may take a moment)")
                
                # Use the OOP service
                service = create_exam_agent_service()
                result = service.analyze_exam_preparation(
                    exam_file_path=exam_path,
                    study_material_paths=study_paths,
                    chat_id=self.session_manager.get_chat_id()
                )
                
                # Display results
                self._display_exam_results(result)
                
                # Cleanup
                cleanup_temp_file(exam_path)
                for path in study_paths:
                    cleanup_temp_file(path)
                    
            except Exception as e:
                st.error(f"Error analyzing exam: {str(e)}")
    
    def _display_exam_results(self, result):
        """Display exam analysis results"""
        st.markdown("### Extracted Topics")
        st.write(", ".join(result.extracted_topics))
        
        st.markdown("### Study Coverage Analysis")
        for topic, recommendation in result.study_recommendations.items():
            st.write(f"**{topic}**: {recommendation}")
        
        st.markdown("### Preparation Suggestions")
        st.write(result.preparation_suggestions)

class EduAgentApp:
    """Main application class that orchestrates the entire UI"""
    
    def __init__(self):
        self.session_manager = UISessionManager()
        self.research_ui = ResearchAgentUI(self.session_manager)
        self.exam_ui = ExamAgentUI(self.session_manager)
    
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(page_title="EduAgent", layout="centered")
    
    def render_header(self):
        """Render the application header"""
        st.title("📚 EduAgent – Multi-Agent Educational Assistant")
        st.markdown("""
        Welcome! This tool helps you:
        - 🧠 Summarize and interact with academic research papers
        - ✍️ Extract study topics from exams and match with your study notes
        """)
        
        st.markdown(f"💬 **Session Chat ID:** `{self.session_manager.get_chat_id()}`")
    
    def render_footer(self):
        """Render the application footer"""
        st.markdown("---")
        st.caption("Created by Valenteno Lenora using LangChain + CrewAI + Mistral + ChromaDB + Streamlit 🧠")
    
    def run(self):
        """Main application entry point"""
        self.setup_page_config()
        self.render_header()
        
        # Create tabs for different agents
        tab1, tab2 = st.tabs(["📄 Research Assistant", "📝 Exam Assistant"])
        
        # Research Agent Tab
        with tab1:
            uploaded_paper = self.research_ui.render_upload_section()
            self.research_ui.process_paper_analysis(uploaded_paper)
            self.research_ui.handle_question_answering()
        
        # Exam Agent Tab
        with tab2:
            uploaded_exam, uploaded_notes = self.exam_ui.render_upload_section()
            self.exam_ui.process_exam_analysis(uploaded_exam, uploaded_notes)
        
        self.render_footer()

# Application entry point
if __name__ == "__main__":
    app = EduAgentApp()
    app.run()