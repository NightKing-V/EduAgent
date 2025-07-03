from langchain_community.llms import Ollama
from langchain_core.language_models.llms import LLM
from functools import lru_cache


@lru_cache(maxsize=1)
def get_llm() -> LLM:

    return Ollama(
        model="mistral",
        temperature=0.4,
        base_url="http://ollama:11434"  # Default Ollama endpoint
    )

