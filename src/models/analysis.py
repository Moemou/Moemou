"""
Analysis and biomarker data models.
"""

from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    """Severity levels for skin conditions."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    VERY_SEVERE = "very_severe"


class Biomarkers(BaseModel):
    """Biomarker measurements for skin analysis."""

    sebum_production: Optional[str] = Field(None, description="Sebum production level (low, normal, high)")
    inflammation_markers: Optional[str] = Field(None, description="Inflammation marker levels")
    skin_ph: Optional[float] = Field(None, description="Skin pH level", ge=3.0, le=9.0)
    hydration_level: Optional[str] = Field(None, description="Skin hydration level")
    microbiome_balance: Optional[str] = Field(None, description="Skin microbiome balance")
    barrier_function: Optional[str] = Field(None, description="Skin barrier function assessment")
    oxidative_stress: Optional[str] = Field(None, description="Oxidative stress markers")
    hormone_indicators: Optional[Dict[str, str]] = Field(None, description="Hormone-related indicators")
    additional_markers: Optional[Dict[str, str]] = Field(None, description="Additional custom biomarkers")


class SkinCondition(BaseModel):
    """Identified skin condition."""

    condition_name: str = Field(..., description="Name of the condition")
    severity: SeverityLevel = Field(..., description="Severity level")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0.0, le=1.0)
    description: str = Field(..., description="Description of the condition")
    affected_areas: List[str] = Field(default_factory=list, description="Affected facial/body areas")
    triggers: List[str] = Field(default_factory=list, description="Potential triggers")
    contributing_factors: List[str] = Field(default_factory=list, description="Contributing factors")


class AnalysisRequest(BaseModel):
    """Request model for skin analysis."""

    user_id: str = Field(..., description="Unique user identifier")
    consultation_id: Optional[str] = Field(None, description="Associated consultation ID")
    symptoms: List[str] = Field(..., description="Observed symptoms")
    biomarkers: Optional[Biomarkers] = Field(None, description="Measured biomarkers")
    images: Optional[List[str]] = Field(None, description="Image URLs or base64 encoded images")
    duration: Optional[str] = Field(None, description="How long the condition has persisted")
    previous_treatments: Optional[List[str]] = Field(None, description="Previously tried treatments")


class AnalysisResponse(BaseModel):
    """Response model for skin analysis."""

    analysis_id: str
    user_id: str
    conditions: List[SkinCondition] = Field(default_factory=list)
    primary_diagnosis: str
    biomarker_interpretation: Dict[str, str] = Field(default_factory=dict)
    root_causes: List[str] = Field(default_factory=list)
    severity_assessment: str
    recommendations_preview: List[str] = Field(default_factory=list)
    requires_professional_care: bool = False
    professional_care_reason: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    analysis_summary: str
    timestamp: str
