import streamlit as st
from typing import Optional
from ui.ResearchAgentUI import ResearchAgentUI
from ui.ExamAgentUI import ExamAgentUI
from ui.UISessionManager import UISessionManager
from ui.chat_panel import render_chat_panel

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
            if uploaded_paper:
                st.info("Please click **Analyze Paper** to continue.")
                
            result = self.research_ui.process_paper_analysis(uploaded_paper)
            
            if result:
                st.session_state["analysis_result"] = result
                
            session_result = st.session_state.get("analysis_result")

            if session_result:
                render_chat_panel(result=session_result, chat_id=self.session_manager.get_chat_id())
        
        
        # Exam Agent Tab
        with tab2:
            # uploaded_exam, uploaded_notes = self.exam_ui.render_upload_section()
            # self.exam_ui.process_exam_analysis(uploaded_exam, uploaded_notes)
            st.write("This feature is under development. Stay tuned!")
        
        self.render_footer()
