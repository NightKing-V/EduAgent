# config/dependencies.py - Dependency injection container
from functools import lru_cache
from services.vector_service import VectorService
from services.research_service import ResearchService
from services.llm_service import LLMService

class DependencyContainer:
    """Simple dependency injection container"""
    
    def __init__(self):
        self._instances = {}
    
    @lru_cache(maxsize=1)
    def get_vector_service(self) -> VectorService:
        """Get singleton vector service"""
        if 'vector_service' not in self._instances:
            self._instances['vector_service'] = VectorService()
        return self._instances['vector_service']
    
    @lru_cache(maxsize=1)
    def get_research_service(self) -> ResearchService:
        """Get singleton research service"""
        if 'research_service' not in self._instances:
            vector_service = self.get_vector_service()
            self._instances['research_service'] = ResearchService(vector_service)
        return self._instances['research_service']
    
    @lru_cache(maxsize=1)
    def get_llm() -> LLM:

        return Ollama(
            model="mistral",
            temperature=0.4,
            base_url="http://ollama:11434"  # Default Ollama endpoint
        )

# Global container instance
container = DependencyContainer()