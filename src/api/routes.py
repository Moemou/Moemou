"""
API routes for the Breakoutlabs skincare agent.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List

from src.models import (
    ConsultationRequest,
    ConsultationResponse,
    AnalysisRequest,
    AnalysisResponse,
    RecommendationResponse,
    ChatRequest,
    ChatResponse,
)
from src.agents import SkincareAgent
from src.llm import get_llm_client
from src.knowledge import KnowledgeBase
from src.config import settings

import uuid
from datetime import datetime


router = APIRouter(prefix=settings.api_prefix, tags=["skincare"])


def get_skincare_agent() -> SkincareAgent:
    """Dependency to get skincare agent instance."""
    llm_client = get_llm_client()
    knowledge_base = KnowledgeBase(knowledge_path=settings.knowledge_base_path)
    return SkincareAgent(llm_client=llm_client, knowledge_base=knowledge_base)


@router.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "name": "Moemou - Breakoutlabs AI Skincare Agent",
        "version": "0.1.0",
        "status": "active",
        "description": "Field-specific AI agent for skincare, dermatology, and acne treatment",
        "features": [
            "Biomarker analysis",
            "Skin condition assessment",
            "Personalized product recommendations",
            "Treatment plan creation",
            "Expert chat support"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "llm_provider": settings.llm_provider,
        "agent_type": settings.agent_type
    }


@router.post("/consultations", response_model=ConsultationResponse)
async def create_consultation(request: ConsultationRequest):
    """
    Start a new skincare consultation.

    This endpoint creates a new consultation session for a user,
    capturing their skin profile and concerns.
    """
    consultation_id = f"consult_{uuid.uuid4().hex[:12]}"

    next_steps = [
        "Complete skin analysis with biomarker data",
        "Receive personalized product recommendations",
        "Get a customized treatment plan",
        "Schedule follow-up assessment"
    ]

    return ConsultationResponse(
        consultation_id=consultation_id,
        user_id=request.user_id,
        status="active",
        message=f"Consultation started successfully. We'll help you achieve clear, healthy skin!",
        next_steps=next_steps,
        created_at=datetime.utcnow()
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_skin(
    request: AnalysisRequest,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Analyze skin condition based on symptoms and biomarkers.

    This endpoint performs a comprehensive analysis of the user's skin,
    interpreting biomarkers and identifying conditions.
    """
    try:
        analysis = await agent.analyze_skin(request)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    analysis: AnalysisResponse,
    user_profile: Dict = None,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Get personalized product recommendations and treatment plan.

    Based on the skin analysis, this endpoint generates specific
    product recommendations and a comprehensive treatment plan.
    """
    try:
        recommendations = await agent.generate_recommendations(
            analysis=analysis,
            user_profile=user_profile
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation generation failed: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Interactive chat with the skincare agent.

    This endpoint allows users to have conversational interactions
    with the AI agent, asking questions and getting expert advice.
    """
    try:
        response = await agent.chat(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


@router.get("/ingredients/{ingredient_name}")
async def get_ingredient_info(
    ingredient_name: str,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Get detailed information about a specific skincare ingredient.

    Returns benefits, usage instructions, contraindications, and
    compatibility with other ingredients.
    """
    ingredient = agent.kb.get_ingredient(ingredient_name)

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail=f"Ingredient '{ingredient_name}' not found in knowledge base"
        )

    return {
        "ingredient_name": ingredient_name,
        "data": ingredient
    }


@router.get("/conditions/{condition_name}")
async def get_condition_info(
    condition_name: str,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Get detailed information about a specific skin condition.

    Returns description, types, causes, treatments, and recommendations.
    """
    condition = agent.kb.get_condition(condition_name)

    if not condition:
        raise HTTPException(
            status_code=404,
            detail=f"Condition '{condition_name}' not found in knowledge base"
        )

    return {
        "condition_name": condition_name,
        "data": condition
    }


@router.get("/products/search")
async def search_products(
    category: str = None,
    concern: str = None,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Search for products by category or skin concern.

    Returns product suggestions based on search criteria.
    """
    if category:
        products = agent.kb.get_product_category(category)
        return {
            "query_type": "category",
            "query": category,
            "results": products
        }

    if concern:
        ingredients = agent.kb.search_ingredients_by_concern(concern)
        return {
            "query_type": "concern",
            "query": concern,
            "recommended_ingredients": ingredients
        }

    raise HTTPException(
        status_code=400,
        detail="Please provide either 'category' or 'concern' parameter"
    )


@router.post("/analyze-biomarkers")
async def analyze_biomarkers(
    biomarkers: Dict,
    skin_type: str = None,
    concerns: List[str] = None,
    age: int = None,
    agent: SkincareAgent = Depends(get_skincare_agent)
):
    """
    Analyze biomarker data and provide interpretation.

    This endpoint focuses specifically on biomarker interpretation
    to help users understand their skin health metrics.
    """
    try:
        from src.models import Biomarkers

        biomarker_obj = Biomarkers(**biomarkers)
        interpretation = agent._interpret_biomarkers(biomarker_obj)

        return {
            "biomarkers": biomarkers,
            "interpretation": interpretation,
            "skin_type": skin_type,
            "concerns": concerns,
            "recommendations": [
                "Use products targeting identified imbalances",
                "Monitor biomarkers regularly to track progress",
                "Adjust routine based on biomarker changes"
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Biomarker analysis failed: {str(e)}"
        )
