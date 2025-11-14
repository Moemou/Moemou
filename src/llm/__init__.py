"""
LLM integration layer for Moemou.
Provides unified interface for different LLM providers.
"""

from .client import LLMClient, get_llm_client
from .prompt_templates import PromptTemplates

__all__ = ["LLMClient", "get_llm_client", "PromptTemplates"]
