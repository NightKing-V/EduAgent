# services/research_service.py - Business logic layer
from typing import List, Dict, Any
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from crewai import Agent, Task, Crew

from core.interfaces import ResearchServiceInterface, VectorSearchInterface, LLMInterface


class ResearchService(ResearchServiceInterface):
    def __init__(self, vector_service: VectorSearchInterface, llm_service: LLMInterface):
        self.vector_service = vector_service
        self.llm = llm_services
        self._crew = None
    
    def _get_crew(self):
        """Lazy initialization of CrewAI components"""
        if self._crew is None:
            # Create agent with tool that uses injected vector service
            def answer_with_llm(question: str, chat_id: str) -> str:
                return self._answer_with_context(question, chat_id)
            
            research_agent = Agent(
                role='AI Research Assistant',
                goal='Answer user questions based on academic papers',
                backstory=(
                    "You are an expert researcher trained on academic papers. "
                    "Provide accurate and concise answers based on uploaded documents."
                ),
                allow_delegation=False,
                verbose=True,
                tools=[answer_with_llm]
            )
            
            research_task = Task(
                description="Answer this user question about the research paper: '{{ question }}'",
                expected_output="A precise and insightful answer using the document's content.",
                agent=research_agent
            )
            
            self._crew = Crew(
                agents=[research_agent],
                tasks=[research_task],
                verbose=True
            )
        
        return self._crew
    
    def _answer_with_context(self, question: str, chat_id: str) -> str:
        """Core QA logic with vector search"""
        docs = self.vector_service.get_query_chunks(
            chat_id=chat_id, 
            query=question, 
            top_k=4
        )
        
        if not docs:
            return "No relevant information found."
        
        chain = load_qa_with_sources_chain(self.llm.get_llm(), chain_type="stuff")
        result = chain(
            {"input_documents": docs, "question": question}, 
            return_only_outputs=True
        )
        return result["answer"]
    
    def answer_question(self, question: str, chat_id: str) -> str:
        """Public method to answer questions using CrewAI"""
        crew = self._get_crew()
        return crew.run({
            "question": question,
            "chat_id": chat_id
        })