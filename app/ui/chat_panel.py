import streamlit as st
from agents.research_agent import create_research_agent_service

def render_chat_panel(chat_id: str, result=None):
    """Display the chat interface with memory support"""
    
    st.markdown("## 💬 Chat with ResearchAgent")
    
    # Initialize chat history if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Inject summary as the first agent message if result is available and not yet added
    if result and not any("summary_intro" in msg for msg in st.session_state.chat_history):
        first_msg = _prepare_first_message(result)
        st.session_state.chat_history.insert(0, {
            "role": "agent",
            "message": first_msg,
            "summary_intro": True  # Tag to avoid duplication
        })

    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        msg = message["message"]

        if role == "user":
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; padding:10px 15px; border-radius:10px; margin-bottom:10px;">
                    <strong>🧑‍🎓 You:</strong><br>{msg}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="border: 1px solid #4CAF50; padding:10px 15px; border-radius:10px; margin-bottom:10px;">
                    <strong>🤖 ResearchAgent:</strong><br>{msg}
                </div>
                """,
                unsafe_allow_html=True
            )


    # Input field
    question = st.text_input("Ask a question about the paper:", key="chat_input")

    # Ask button
    if st.button("Ask"):
        if question.strip():
            with st.spinner("ResearchAgent is thinking..."):
                try:
                    agent = create_research_agent_service()
                    answer = agent.ask_question(question=question, chat_id=chat_id)

                    # Update session chat history
                    st.session_state.chat_history.append({"role": "user", "message": question})
                    st.session_state.chat_history.append({"role": "agent", "message": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Agent error: {e}")
        else:
            st.warning("Please enter a question.")

    # Reset chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


def _prepare_first_message(result) -> str:
    """Prepare the summary + topics as the first agent message."""
    summary = f"📄 **Paper Summary:**\n{result.summary}"

    if isinstance(result.topics, list):
        topics_str = ', '.join(result.topics)
    elif isinstance(result.topics, str):
        topics_str = result.topics
    else:
        topics_str = str(result.topics)  # fallback
    
    topics = f"\n\n🧠 **Topics Covered:**\n{topics_str}"
    chunks = f"\n\n📊 **Processed Chunks:** {result.chunk_count}"
    return summary + topics + chunks

