"""
Recommendation and treatment plan data models.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ProductRecommendation(BaseModel):
    """Recommended skincare product."""

    product_name: str
    category: str = Field(..., description="Product category (cleanser, moisturizer, treatment, etc.)")
    key_ingredients: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    suitable_for: List[str] = Field(default_factory=list, description="Skin types/conditions")
    application_instructions: str
    frequency: str = Field(..., description="How often to use")
    contraindications: List[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Why this product is recommended")
    alternatives: Optional[List[str]] = Field(None, description="Alternative product suggestions")


class RoutineStep(BaseModel):
    """Step in a skincare routine."""

    step_number: int
    time_of_day: str = Field(..., description="AM, PM, or both")
    action: str = Field(..., description="What to do (cleanse, treat, moisturize, etc.)")
    products: List[str] = Field(default_factory=list)
    instructions: str
    duration: Optional[str] = Field(None, description="How long the step takes")
    tips: List[str] = Field(default_factory=list)


class TreatmentPlan(BaseModel):
    """Comprehensive treatment plan."""

    plan_id: str
    plan_name: str
    duration: str = Field(..., description="Expected duration (e.g., '4-6 weeks')")
    primary_goals: List[str] = Field(default_factory=list)
    morning_routine: List[RoutineStep] = Field(default_factory=list)
    evening_routine: List[RoutineStep] = Field(default_factory=list)
    weekly_treatments: Optional[List[RoutineStep]] = Field(None)
    lifestyle_recommendations: List[str] = Field(default_factory=list)
    dietary_suggestions: Optional[List[str]] = Field(None)
    expected_timeline: Dict[str, str] = Field(default_factory=dict)
    monitoring_metrics: List[str] = Field(default_factory=list)
    adjustment_triggers: List[str] = Field(default_factory=list, description="When to adjust the plan")


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""

    recommendation_id: str
    user_id: str
    products: List[ProductRecommendation] = Field(default_factory=list)
    treatment_plan: Optional[TreatmentPlan] = None
    key_ingredients_to_use: List[str] = Field(default_factory=list)
    ingredients_to_avoid: List[str] = Field(default_factory=list)
    timeline: str
    expected_results: str
    follow_up_schedule: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    important_notes: List[str] = Field(default_factory=list)
    timestamp: str
