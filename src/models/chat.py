"""
Chat interaction data models.
"""

from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role in conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Individual chat message."""

    role: MessageRole
    content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    """Request model for chat interaction."""

    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., description="User's message")
    consultation_id: Optional[str] = Field(None, description="Associated consultation ID")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        description="Previous conversation context"
    )
    include_analysis: bool = Field(
        default=False,
        description="Whether to include detailed analysis in response"
    )


class ChatResponse(BaseModel):
    """Response model for chat interaction."""

    response: str = Field(..., description="Agent's response")
    conversation_id: str = Field(..., description="Conversation identifier")
    suggestions: List[str] = Field(default_factory=list, description="Suggested follow-up questions")
    action_items: List[str] = Field(default_factory=list, description="Recommended actions")
    referenced_knowledge: List[str] = Field(
        default_factory=list,
        description="Knowledge base sources referenced"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    requires_clarification: bool = Field(default=False)
    clarification_questions: Optional[List[str]] = Field(None)
    timestamp: str
