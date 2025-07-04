from abc import ABC, abstractmethod
from typing import List, Union
from llm.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate

class TextProcessor(ABC):
    
    def __init__(self):
        self.llm = get_llm()
    
    @abstractmethod
    def process(self, text: Union[str, List[str]]) -> str:
        pass

class TextSummarizer(TextProcessor):
    
    def process(self, text: Union[str, List[str]]) -> str:
        # Handle both string and list inputs
        content = "\n\n".join(text) if isinstance(text, list) else text
        
        prompt = ChatPromptTemplate.from_template("""
        You are an academic summarizer. Summarize the following paper content briefly.

        Include:
        - Objective
        - Key contributions
        - Methodology
        - Conclusions

        TEXT:
        {text}
        """)
        return self.llm.invoke(prompt.format(text=content))

class TopicExtractor(TextProcessor):
    
    def process(self, text: Union[str, List[str]]) -> str:
        content = "\n\n".join(text) if isinstance(text, list) else text
        
        prompt = ChatPromptTemplate.from_template("""
        You are a research assistant. From the text below, extract:
        - Main Topics
        - Techniques/Methods used
        - Keywords

        TEXT:
        {text}
        """)
        return self.llm.invoke(prompt.format(text=content))

class TextProcessorService:
    """Service class that coordinates text processing operations"""
    
    def __init__(self):
        self.summarizer = TextSummarizer()
        self.topic_extractor = TopicExtractor()
    
    def summarize_text(self, text: Union[str, List[str]]) -> str:
        return self.summarizer.process(text)
    
    def extract_topics(self, text: Union[str, List[str]]) -> str:
        return self.topic_extractor.process(text)

# Factory function for backward compatibility
def create_text_processor() -> TextProcessorService:
    return TextProcessorService()