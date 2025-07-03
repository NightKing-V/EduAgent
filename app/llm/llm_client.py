# app/llm/llm_client.py
from abc import ABC, abstractmethod
from langchain_community.llms import Ollama
from langchain_core.language_models.llms import LLM
from functools import lru_cache
from typing import Dict, Any, Optional

class LLMProvider(ABC):
    """Abstract base class for LLM providers (Strategy Pattern)"""
    
    @abstractmethod
    def create_llm(self, **kwargs) -> LLM:
        pass

class OllamaProvider(LLMProvider):
    """Concrete implementation for Ollama"""
    
    def create_llm(self, model: str = "mistral", temperature: float = 0.4, base_url: str = "http://ollama:11434") -> LLM:
        return Ollama(
            model=model,
            temperature=temperature,
            base_url=base_url
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