"""
Consultation data models.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ConsultationRequest(BaseModel):
    """Request model for starting a new consultation."""

    user_id: str = Field(..., description="Unique user identifier")
    skin_type: Optional[str] = Field(None, description="User's skin type (oily, dry, combination, normal)")
    concerns: List[str] = Field(default_factory=list, description="Primary skin concerns")
    current_products: Optional[List[str]] = Field(None, description="Currently used products")
    allergies: Optional[List[str]] = Field(None, description="Known allergies or sensitivities")
    medical_conditions: Optional[List[str]] = Field(None, description="Relevant medical conditions")
    age: Optional[int] = Field(None, description="User's age", ge=13, le=120)
    additional_info: Optional[str] = Field(None, description="Any additional information")


class Consultation(BaseModel):
    """Internal consultation model."""

    consultation_id: str
    user_id: str
    skin_type: Optional[str] = None
    concerns: List[str] = Field(default_factory=list)
    current_products: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    medical_conditions: List[str] = Field(default_factory=list)
    age: Optional[int] = None
    additional_info: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"


class ConsultationResponse(BaseModel):
    """Response model for consultation creation."""

    consultation_id: str
    user_id: str
    status: str
    message: str
    next_steps: List[str] = Field(default_factory=list)
    created_at: datetime
