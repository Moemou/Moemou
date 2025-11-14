"""
LLM client implementation supporting multiple providers.
"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import openai
from anthropic import Anthropic

from src.config import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Generate a streaming response from the LLM."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI LLM client implementation."""

    def __init__(self, api_key: str, model: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate a response using OpenAI API."""
        temp = temperature if temperature is not None else settings.llm_temperature
        tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            **kwargs
        )
        return response.choices[0].message.content

    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Generate a streaming response using OpenAI API."""
        temp = temperature if temperature is not None else settings.llm_temperature
        tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            stream=True,
            **kwargs
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicClient(LLMClient):
    """Anthropic Claude LLM client implementation."""

    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate a response using Anthropic API."""
        temp = temperature if temperature is not None else settings.llm_temperature
        tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

        # Extract system message if present
        system_message = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=tokens,
            temperature=temp,
            system=system_message or "",
            messages=user_messages,
            **kwargs
        )
        return response.content[0].text

    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """Generate a streaming response using Anthropic API."""
        temp = temperature if temperature is not None else settings.llm_temperature
        tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

        # Extract system message if present
        system_message = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        with self.client.messages.stream(
            model=self.model,
            max_tokens=tokens,
            temperature=temp,
            system=system_message or "",
            messages=user_messages,
            **kwargs
        ) as stream:
            for text in stream.text_stream:
                yield text


def get_llm_client() -> LLMClient:
    """
    Factory function to get the appropriate LLM client based on configuration.

    Returns:
        LLMClient: Configured LLM client instance

    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    provider = settings.llm_provider

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured")
        return OpenAIClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model
        )
    elif provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("Anthropic API key is not configured")
        return AnthropicClient(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
