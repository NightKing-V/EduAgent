from app.llm.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = get_llm()

def summarize_text(text: str) -> str:
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
    return llm.invoke(prompt.format(text=text))

# LangChain Tool wrapper
summarizer_tool = Tool(
    name="PaperSummarizer",
    func=summarize_text,
    description="Summarizes an academic paper's objective, contributions, and results."
)
