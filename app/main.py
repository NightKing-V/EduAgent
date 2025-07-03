# ui/streamlit_app.py - Clean UI layer
import streamlit as st
import os
import sys

# 📌 Make sure Python can find other app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from utils.uuid_gen import generate_uuid
from utils.file_handler import cleanup_temp_file, save_uploaded_file_temporarily
# from agents.research_agent import run_research_qna
# from pipelines.ingestion_pipeline import run_ingestion_pipeline


# Initialize chat ID only once per session
if "chat_id" not in st.session_state:
    st.session_state.chat_id = generate_uuid()

st.markdown(f"💬 **Session Chat ID:** `{st.session_state.chat_id}`")

# Set Streamlit page config
st.set_page_config(page_title="EduAgent", layout="centered")

# Title and description
st.title("📚 EduAgent – Multi-Agent Educational Assistant")
st.markdown("""
Welcome! This tool helps you:
- 🧠 Summarize and interact with academic research papers
- ✍️ Extract study topics from exams and match with your study notes
""")

# Tabs for different agents
tab1, tab2 = st.tabs(["📄 Research Assistant", "📝 Exam Assistant"])

# --- Research Agent UI ---
with tab1:
    st.subheader("Upload a Research Paper (PDF)")
    uploaded_paper = st.file_uploader("Choose a PDF file", type=["pdf"], key="research_pdf")
    print(f"Uploaded paper: {uploaded_paper}")

    if uploaded_paper is not None:
        st.success("✅ Paper uploaded. Ready to summarize and chat with the agent.")
        
        if st.button("🔍 Analyze Paper"):
            
            temp_pdf_path = save_uploaded_file_temporarily(uploaded_file = uploaded_paper, chat_id=st.session_state.chat_id)
            
            from pipelines.ingestion_pipeline import run_ingestion_pipeline
            
            st.info("Running ResearchAgent... (this may take a moment)")
            ingestion_result = run_ingestion_pipeline(
                file_path=temp_pdf_path,
                chat_id=st.session_state.chat_id
            )
            
            cleanup_temp_file(temp_pdf_path)
            
            st.markdown("### Paper Summary")
            st.write(ingestion_result["summary"])
            
            st.markdown("### Extracted Topics")
            st.write(", ".join(ingestion_result["topics"]))
        
        question = st.text_input("Ask a question about the research paper:")

        if st.button("Ask ResearchAgent") and question.strip():
            from agents.research_agent import run_research_qna
            with st.spinner("ResearchAgent is thinking..."):
                try:
                    
                    answer = run_research_qna(
                        question=question,
                        chat_id=st.session_state.chat_id
                    )
                    
                    st.markdown("### Answer:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error running ResearchAgent: {e}")

# --- Exam Agent UI ---
with tab2:
    st.subheader("Upload Exam Paper and Study Materials")
    uploaded_exam = st.file_uploader("Upload exam paper (PDF or TXT)", type=["pdf", "txt"], key="exam_pdf")
    uploaded_notes = st.file_uploader("Upload study material (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True, key="study_materials")

    if uploaded_exam is not None and uploaded_notes:
        st.success("✅ Exam and materials uploaded.")
        if st.button("🧠 Analyze Exam & Match Study Areas"):
            st.info("Running ExamAgent... (placeholder)")

# Footer
st.markdown("---")
st.caption("Created by Valenteno Lenora using LangChain + CrewAI + Mistral + ChromaDB + Streamlit 🧠")
