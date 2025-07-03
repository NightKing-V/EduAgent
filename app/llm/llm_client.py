# app/llm/llm_client.py
from abc import ABC, abstractmethod
from langchain_community.llms import Ollama
from langchain_core.language_models.llms import LLM
from functools import lru_cache
from typing import Dict, Any, Optional
import os

class LLMProvider(ABC):
    """Abstract base class for LLM providers (Strategy Pattern)"""
    
    @abstractmethod
    def create_llm(self, **kwargs) -> LLM:
        pass

class OllamaProvider(LLMProvider):
    """Concrete implementation for Ollama with CrewAI compatibility"""
    
    def create_llm(self, model: str = "mistral", temperature: float = 0.4, base_url: str = "http://ollama:11434") -> LLM:
        return Ollama(
            model=model,
            temperature=temperature,
            base_url=base_url,
            # Add timeout and other stability parameters
            timeout=60,
            keep_alive=True
        )

class LLMFactory:
    """Factory class for creating LLM instances"""
    
    _providers: Dict[str, LLMProvider] = {
        "ollama": OllamaProvider()
    }
    
    @classmethod
    def register_provider(cls, name: str, provider: LLMProvider):
        """Register a new LLM provider"""
        cls._providers[name] = provider
    
    @classmethod
    def create_llm(cls, provider_name: str = "ollama", **kwargs) -> LLM:
        """Create an LLM instance using the specified provider"""
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        return cls._providers[provider_name].create_llm(**kwargs)

@lru_cache(maxsize=1)
def get_llm(provider: str = "ollama", **kwargs) -> LLM:
    """Get cached LLM instance"""
    return LLMFactory.create_llm(provider, **kwargs)

# CrewAI-specific configuration
def get_crewai_llm(model: str = "mistral", temperature: float = 0.4, base_url: str = "http://ollama:11434"):
    """
    Get an LLM instance specifically configured for CrewAI.
    
    This function creates an LLM that works with CrewAI by using the proper
    model identifier format that litellm expects.
    """
    # Set environment variable for CrewAI/litellm compatibility
    os.environ["OLLAMA_BASE_URL"] = base_url
    
    # Create Ollama instance with model name in format that CrewAI/litellm expects
    llm = Ollama(
        model=f"ollama/{model}",  # This is the key fix - prefix with provider name
        temperature=temperature,
        base_url=base_url,
        timeout=60,
        keep_alive=True
    )
    
    return llm