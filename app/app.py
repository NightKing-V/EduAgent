import streamlit as st

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

    if uploaded_paper is not None:
        st.success("✅ Paper uploaded. Ready to summarize and chat with the agent.")
        # Placeholder button to trigger research agent
        if st.button("🔍 Analyze Paper"):
            st.info("Running ResearchAgent... (placeholder)")
            
            
            # Call your agent here later



# --- Exam Agent UI ---
with tab2:
    st.subheader("Upload Exam Paper and Study Materials")
    uploaded_exam = st.file_uploader("Upload exam paper (PDF or TXT)", type=["pdf", "txt"], key="exam_pdf")
    uploaded_notes = st.file_uploader("Upload study material (PDF or TXT)", type=["pdf", "txt"], accept_multiple_files=True, key="study_materials")

    if uploaded_exam is not None and uploaded_notes:
        st.success("✅ Exam and materials uploaded.")
        if st.button("🧠 Analyze Exam & Match Study Areas"):
            st.info("Running ExamAgent... (placeholder)")
            
            
            # Call your agent here later


# Footer
st.markdown("---")
st.caption("Created by Valenteno Lenora using LangChain + CrewAI + Mistral + ChromaDB + Streamlit 🧠")
