from crewai import Agent, Task, Crew
from app.tools.vector_search import get_query_chunks
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from app.llm.llm_client import get_llm# or use your preferred LLM

# Load your LLM instance
llm = get_llm()  # Replace with your own LLM if needed

# Define a function-based tool (simple callable)
def answer_with_llm(question: str, chat_id: str) -> str:
    docs = get_query_chunks(chat_id=chat_id, query=question, top_k=4)
    if not docs:
        return "No relevant information found."

    chain = load_qa_with_sources_chain(llm, chain_type="stuff")
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result["answer"]

# Create an Agent
research_agent = Agent(
    role='AI Research Assistant',
    goal='Answer user questions based on academic papers already processed into the system',
    backstory=(
        "You are an expert researcher trained on thousands of academic papers. "
        "Your task is to give accurate and concise answers based on uploaded documents using vector search and reasoning."
    ),
    allow_delegation=False,
    verbose=True,
    tools=[answer_with_llm]  # ✅ Use function directly, not Command
)

# Define a task template that will dynamically receive user input
research_task = Task(
    description="Answer this user question about the research paper: '{{ question }}'",
    expected_output="A precise and insightful answer using the document's content.",
    agent=research_agent
)

# Create a Crew (you can call this in Streamlit later)
crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True
)


def run_research_qna(question: str, chat_id: str):
    return crew.run({
        "question": question,
        "chat_id": chat_id
    })