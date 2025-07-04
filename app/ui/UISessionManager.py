
from utils.uuid_gen import generate_uuid
import streamlit as st


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