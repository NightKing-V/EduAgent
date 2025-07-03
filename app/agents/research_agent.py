# app/agents/research_agent.py
from typing import Optional
from dataclasses import dataclass
from crewai import Agent, Task, Crew
from services.vector_store_service import VectorStoreService, create_vector_store_service
from llm.llm_client import get_crewai_llm

@dataclass
class ResearchQuery:
    """Data class for research queries"""
    question: str
    chat_id: str
    top_k: int = 4

class ResearchAgent:
    """
    Research agent with better separation of concerns and dependency injection.
    Follows Single Responsibility Principle.
    """
    
    def __init__(self, vector_store_service: VectorStoreService):
        self.vector_store_service = vector_store_service
        self.llm = get_crewai_llm()  # Use CrewAI-compatible LLM
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        return Agent(
            role='AI Research Assistant',
            goal='Answer user questions based on academic papers already processed into the system',
            backstory=(
                "You are an expert researcher trained on thousands of academic papers. "
                "You use your knowledge to give accurate, insightful answers based on "
                "the context provided in the task."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )
    
    def _get_relevant_context(self, query: ResearchQuery) -> str:
        """Retrieve relevant documents and create context"""
        docs = self.vector_store_service.get_query_chunks(
            chat_id=query.chat_id,
            query=query.question,
            top_k=query.top_k
        )
        
        if not docs:
            return "No relevant information found in the knowledge base."
        
        return "\n\n".join([doc.page_content for doc in docs])
    
    def _create_research_task(self, query: ResearchQuery, context: str) -> Task:
        """Create a research task with the given context"""
        return Task(
            description=f"""
            Answer this user question about the research paper: '{query.question}'
            
            Use the following context from the research papers:
            
            {context}
            
            Provide a precise and insightful answer based on the context provided.
            If the context doesn't contain enough information to answer the question,
            clearly state what information is missing.
            """,
            expected_output="A precise and insightful answer using the document's content.",
            agent=self.agent
        )
    
    def answer_question(self, query: ResearchQuery) -> str:
        """
        Answer a research question using the knowledge base.
        
        Args:
            query: ResearchQuery object containing the question and metadata
            
        Returns:
            String answer from the research agent
        """
        # Get relevant context
        context = self._get_relevant_context(query)
        
        if context == "No relevant information found in the knowledge base.":
            return context
        
        # Create and execute task
        task = self._create_research_task(query, context)
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return str(result)

class ResearchAgentService:
    """Service class for managing research agent operations"""
    
    def __init__(self, vector_store_service: Optional[VectorStoreService] = None):
        self.vector_store_service = vector_store_service or create_vector_store_service()
        self.research_agent = ResearchAgent(self.vector_store_service)
    
    def ask_question(self, question: str, chat_id: str, top_k: int = 4) -> str:
        """Convenience method for asking questions"""
        query = ResearchQuery(
            question=question,
            chat_id=chat_id,
            top_k=top_k
        )
        return self.research_agent.answer_question(query)

# Factory function
def create_research_agent_service() -> ResearchAgentService:
    """Create a research agent service with default configuration"""
    return ResearchAgentService()

# Backward compatibility function
def run_research_qna(question: str, chat_id: str) -> str:
    """Legacy function for backward compatibility"""
    service = create_research_agent_service()
    return service.ask_question(question, chat_id)