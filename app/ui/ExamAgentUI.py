from utils.file_handler import cleanup_temp_file, save_uploaded_file_temporarily
import streamlit as st
from ui.UISessionManager import UISessionManager

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
