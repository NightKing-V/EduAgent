from app.llm.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = get_llm()

def extract_topics(text: str) -> str:
    prompt = ChatPromptTemplate.from_template("""
    You are a research assistant. From the text below, extract:
    - Main Topics
    - Techniques/Methods used
    - Keywords

    TEXT:
    {text}
    """)
    return llm.invoke(prompt.format(text=text))

# LangChain Tool wrapper
topic_extractor_tool = Tool(
    name="TopicExtractor",
    func=extract_topics,
    description="Extracts key topics, methods, and keywords from academic text."
)
