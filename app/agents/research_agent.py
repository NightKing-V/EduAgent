from crewai import Agent, Task, Crew
from app.tools.vector_search import get_query_chunks
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from app.llm.llm_client import get_llm

llm = get_llm()

# Create agent without tools - let it use the LLM directly
research_agent = Agent(
    role='AI Research Assistant',
    goal='Answer user questions based on academic papers already processed into the system',
    backstory=(
        "You are an expert researcher trained on thousands of academic papers. "
        "You use your knowledge to give accurate, insightful answers based on "
        "the context provided in the task."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm  # Pass the LLM directly to the agent
)

def run_research_qna(question: str, chat_id: str):
    # Get relevant documents
    docs = get_query_chunks(chat_id=chat_id, query=question, top_k=4)
    
    if not docs:
        return "No relevant information found."
    
    # Create context from documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Create task with context included
    research_task = Task(
        description=f"""
        Answer this user question about the research paper: '{question}'
        
        Use the following context from the research papers:
        
        {context}
        
        Provide a precise and insightful answer based on the context provided.
        """,
        expected_output="A precise and insightful answer using the document's content.",
        agent=research_agent
    )
    
    crew = Crew(
        agents=[research_agent],
        tasks=[research_task],
        verbose=True
    )
    
    result = crew.kickoff()
    return result