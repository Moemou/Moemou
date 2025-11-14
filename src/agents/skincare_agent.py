"""
Breakoutlabs Skincare Agent - Field-specific AI expert for dermatology and acne treatment.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.llm import LLMClient, PromptTemplates
from src.knowledge import KnowledgeBase
from src.models import (
    AnalysisRequest,
    AnalysisResponse,
    SkinCondition,
    SeverityLevel,
    Biomarkers,
    ProductRecommendation,
    RecommendationResponse,
    TreatmentPlan,
    RoutineStep,
    ChatRequest,
    ChatResponse,
)


class SkincareAgent:
    """
    Intelligent skincare agent with dermatology expertise.
    Specializes in acne treatment, biomarker analysis, and personalized recommendations.
    """

    def __init__(self, llm_client: LLMClient, knowledge_base: KnowledgeBase):
        self.llm = llm_client
        self.kb = knowledge_base
        self.prompt_templates = PromptTemplates()

    async def analyze_skin(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Perform comprehensive skin analysis based on symptoms and biomarkers.

        Args:
            request: Analysis request with symptoms and biomarker data

        Returns:
            Detailed analysis response with diagnoses and recommendations
        """
        # Prepare biomarker interpretation
        biomarker_interpretation = {}
        if request.biomarkers:
            biomarker_interpretation = self._interpret_biomarkers(request.biomarkers)

        # Build analysis prompt
        biomarker_str = json.dumps(request.biomarkers.dict() if request.biomarkers else {}, indent=2)
        prompt = self.prompt_templates.format_skin_analysis(
            symptoms=request.symptoms,
            duration=request.duration,
            previous_treatments=request.previous_treatments,
            biomarkers=biomarker_str
        )

        # Get LLM analysis
        messages = [
            {"role": "system", "content": PromptTemplates.SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        llm_response = await self.llm.generate_response(messages, temperature=0.7)

        # Parse response and identify conditions
        conditions = self._identify_conditions(llm_response, request.symptoms)

        # Determine primary diagnosis
        primary_diagnosis = conditions[0].condition_name if conditions else "Unable to determine"
        severity_assessment = conditions[0].severity.value if conditions else "unknown"

        # Check if professional care is needed
        requires_professional = self._requires_professional_care(conditions, request.symptoms)

        # Generate analysis ID
        analysis_id = f"analysis_{uuid.uuid4().hex[:12]}"

        return AnalysisResponse(
            analysis_id=analysis_id,
            user_id=request.user_id,
            conditions=conditions,
            primary_diagnosis=primary_diagnosis,
            biomarker_interpretation=biomarker_interpretation,
            root_causes=self._extract_root_causes(conditions),
            severity_assessment=severity_assessment,
            recommendations_preview=self._generate_recommendations_preview(conditions),
            requires_professional_care=requires_professional,
            professional_care_reason=self._get_professional_care_reason(conditions, request.symptoms) if requires_professional else None,
            confidence_score=self._calculate_confidence(conditions),
            analysis_summary=llm_response[:500],  # First 500 chars as summary
            timestamp=datetime.utcnow().isoformat()
        )

    async def generate_recommendations(
        self,
        analysis: AnalysisResponse,
        user_profile: Optional[Dict] = None
    ) -> RecommendationResponse:
        """
        Generate personalized product recommendations and treatment plan.

        Args:
            analysis: Previous skin analysis result
            user_profile: Optional user profile with preferences

        Returns:
            Comprehensive recommendations including products and treatment plan
        """
        # Get relevant ingredients from knowledge base
        primary_condition = analysis.primary_diagnosis.lower()
        acne_treatments = self.kb.get_acne_treatments() if "acne" in primary_condition else {}

        # Build recommendation prompt
        biomarker_summary = json.dumps(analysis.biomarker_interpretation, indent=2)
        skin_analysis = f"{analysis.primary_diagnosis} ({analysis.severity_assessment})\n"
        skin_analysis += f"Root causes: {', '.join(analysis.root_causes)}"

        prompt = self.prompt_templates.format_product_recommendation(
            skin_analysis=skin_analysis,
            biomarker_summary=biomarker_summary,
            user_preferences=user_profile,
            allergies=user_profile.get("allergies", []) if user_profile else None,
            budget=user_profile.get("budget") if user_profile else None
        )

        messages = [
            {"role": "system", "content": PromptTemplates.SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        llm_response = await self.llm.generate_response(messages, temperature=0.7)

        # Generate product recommendations
        products = self._generate_product_recommendations(
            analysis,
            acne_treatments,
            user_profile
        )

        # Generate treatment plan
        treatment_plan = await self._generate_treatment_plan(analysis, user_profile)

        # Extract key ingredients
        key_ingredients = self._extract_key_ingredients(analysis)
        ingredients_to_avoid = self._get_ingredients_to_avoid(user_profile)

        recommendation_id = f"rec_{uuid.uuid4().hex[:12]}"

        return RecommendationResponse(
            recommendation_id=recommendation_id,
            user_id=analysis.user_id,
            products=products,
            treatment_plan=treatment_plan,
            key_ingredients_to_use=key_ingredients,
            ingredients_to_avoid=ingredients_to_avoid,
            timeline="4-8 weeks for initial improvement, 12-16 weeks for significant results",
            expected_results=llm_response[:300],
            follow_up_schedule=[
                "Week 2: Check for irritation or adverse reactions",
                "Week 4: Assess initial response",
                "Week 8: Evaluate progress and adjust if needed",
                "Week 12: Full re-assessment"
            ],
            warnings=self._generate_warnings(key_ingredients),
            important_notes=self._generate_important_notes(analysis),
            timestamp=datetime.utcnow().isoformat()
        )

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Handle conversational interactions with the skincare agent.

        Args:
            request: Chat request with user message and context

        Returns:
            Conversational response with suggestions and action items
        """
        # Build conversation context
        messages = [{"role": "system", "content": PromptTemplates.SYSTEM_PROMPT}]

        # Add conversation history
        for msg in request.conversation_history[-5:]:  # Last 5 messages
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })

        # Generate response
        llm_response = await self.llm.generate_response(messages, temperature=0.8)

        # Extract suggestions and action items
        suggestions = self._extract_suggestions(llm_response)
        action_items = self._extract_action_items(request.message, llm_response)

        # Determine if clarification is needed
        requires_clarification = self._check_needs_clarification(request.message)
        clarification_questions = self._generate_clarification_questions(request.message) if requires_clarification else None

        conversation_id = request.consultation_id or f"chat_{uuid.uuid4().hex[:12]}"

        return ChatResponse(
            response=llm_response,
            conversation_id=conversation_id,
            suggestions=suggestions,
            action_items=action_items,
            referenced_knowledge=self._get_referenced_knowledge(request.message),
            confidence=0.85,  # Base confidence
            requires_clarification=requires_clarification,
            clarification_questions=clarification_questions,
            timestamp=datetime.utcnow().isoformat()
        )

    def _interpret_biomarkers(self, biomarkers: Biomarkers) -> Dict[str, str]:
        """Interpret biomarker values using knowledge base."""
        interpretations = {}

        if biomarkers.sebum_production:
            interp = self.kb.interpret_biomarker("sebum_production", biomarkers.sebum_production)
            if interp:
                interpretations["sebum_production"] = interp

        if biomarkers.inflammation_markers:
            interp = self.kb.interpret_biomarker("inflammation_markers", biomarkers.inflammation_markers)
            if interp:
                interpretations["inflammation_markers"] = interp

        if biomarkers.skin_ph:
            ph_value = biomarkers.skin_ph
            if ph_value < 4.5:
                interpretations["skin_ph"] = "Acidic - May indicate irritation or over-exfoliation"
            elif 4.5 <= ph_value <= 5.5:
                interpretations["skin_ph"] = "Optimal - Healthy acid mantle"
            else:
                interpretations["skin_ph"] = "Alkaline - Compromised barrier, acne risk"

        if biomarkers.hydration_level:
            interp = self.kb.interpret_biomarker("hydration_level", biomarkers.hydration_level)
            if interp:
                interpretations["hydration_level"] = interp

        if biomarkers.microbiome_balance:
            interp = self.kb.interpret_biomarker("microbiome_balance", biomarkers.microbiome_balance)
            if interp:
                interpretations["microbiome_balance"] = interp

        return interpretations

    def _identify_conditions(self, llm_response: str, symptoms: List[str]) -> List[SkinCondition]:
        """Identify skin conditions from analysis."""
        conditions = []

        # Check for acne in symptoms or response
        if any(term in " ".join(symptoms).lower() for term in ["acne", "pimple", "breakout", "blemish"]):
            acne_info = self.kb.get_condition("acne")
            if acne_info:
                # Determine severity based on symptoms
                severity = self._determine_acne_severity(symptoms, llm_response)

                conditions.append(SkinCondition(
                    condition_name="Acne Vulgaris",
                    severity=severity,
                    confidence=0.85,
                    description=acne_info.get("description", ""),
                    affected_areas=["face", "jawline", "forehead"],
                    triggers=acne_info.get("root_causes", [])[:3],
                    contributing_factors=acne_info.get("root_causes", [])[3:6]
                ))

        return conditions if conditions else [
            SkinCondition(
                condition_name="General Skin Concern",
                severity=SeverityLevel.MILD,
                confidence=0.5,
                description="Requires more information for accurate diagnosis",
                affected_areas=[],
                triggers=[],
                contributing_factors=[]
            )
        ]

    def _determine_acne_severity(self, symptoms: List[str], llm_response: str) -> SeverityLevel:
        """Determine acne severity from symptoms."""
        symptoms_text = " ".join(symptoms).lower() + " " + llm_response.lower()

        if any(term in symptoms_text for term in ["cystic", "nodule", "severe", "scarring"]):
            return SeverityLevel.SEVERE
        elif any(term in symptoms_text for term in ["moderate", "inflammatory", "pustule"]):
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MILD

    def _requires_professional_care(self, conditions: List[SkinCondition], symptoms: List[str]) -> bool:
        """Determine if professional medical care is needed."""
        # Check severity
        for condition in conditions:
            if condition.severity in [SeverityLevel.SEVERE, SeverityLevel.VERY_SEVERE]:
                return True

        # Check for red flags
        symptoms_text = " ".join(symptoms).lower()
        red_flags = ["cystic", "nodule", "severe pain", "fever", "spreading rapidly", "not responding"]

        return any(flag in symptoms_text for flag in red_flags)

    def _get_professional_care_reason(self, conditions: List[SkinCondition], symptoms: List[str]) -> str:
        """Get reason for professional care recommendation."""
        for condition in conditions:
            if condition.severity == SeverityLevel.SEVERE:
                return "Severe condition requiring prescription medication and medical supervision"

        return "Condition severity or symptoms suggest professional evaluation would be beneficial"

    def _extract_root_causes(self, conditions: List[SkinCondition]) -> List[str]:
        """Extract root causes from identified conditions."""
        causes = []
        for condition in conditions:
            causes.extend(condition.contributing_factors[:3])
        return list(set(causes))[:5]  # Top 5 unique causes

    def _generate_recommendations_preview(self, conditions: List[SkinCondition]) -> List[str]:
        """Generate quick recommendations preview."""
        return [
            "Use gentle, pH-balanced cleanser",
            "Incorporate niacinamide for oil control",
            "Apply salicylic acid for exfoliation",
            "Moisturize to support skin barrier",
            "Always use SPF 30+ sunscreen"
        ]

    def _calculate_confidence(self, conditions: List[SkinCondition]) -> float:
        """Calculate overall confidence score."""
        if not conditions:
            return 0.5
        return sum(c.confidence for c in conditions) / len(conditions)

    def _generate_product_recommendations(
        self,
        analysis: AnalysisResponse,
        acne_treatments: Dict,
        user_profile: Optional[Dict]
    ) -> List[ProductRecommendation]:
        """Generate specific product recommendations."""
        products = []

        # Recommend cleanser
        products.append(ProductRecommendation(
            product_name="Gentle Salicylic Acid Cleanser",
            category="cleanser",
            key_ingredients=["salicylic_acid", "niacinamide"],
            benefits=["Unclogs pores", "Reduces oil", "Prevents breakouts"],
            suitable_for=["oily", "acne-prone"],
            application_instructions="Use AM and PM. Massage onto damp skin, rinse thoroughly.",
            frequency="Twice daily",
            contraindications=["Aspirin allergy"],
            confidence_score=0.9,
            reasoning="Salicylic acid is essential for acne treatment as it exfoliates inside pores",
            alternatives=["Gentle cream cleanser for sensitive skin"]
        ))

        # Recommend niacinamide treatment
        products.append(ProductRecommendation(
            product_name="10% Niacinamide Serum",
            category="treatment",
            key_ingredients=["niacinamide"],
            benefits=["Reduces sebum", "Minimizes pores", "Fades marks", "Anti-inflammatory"],
            suitable_for=["all skin types"],
            application_instructions="Apply to clean skin AM and PM before moisturizer",
            frequency="Twice daily",
            contraindications=[],
            confidence_score=0.95,
            reasoning="Niacinamide is proven to reduce sebum production and inflammation in acne",
            alternatives=["Azelaic acid for sensitive skin"]
        ))

        # Add retinoid for moderate to severe acne
        if analysis.severity_assessment in ["moderate", "severe"]:
            products.append(ProductRecommendation(
                product_name="Retinoid Treatment",
                category="treatment",
                key_ingredients=["retinoids"],
                benefits=["Treats acne", "Prevents breakouts", "Improves texture"],
                suitable_for=["acne-prone"],
                application_instructions="Start 2x per week PM only. Apply pea-sized amount to dry skin.",
                frequency="2-3 times weekly initially, build up to nightly",
                contraindications=["Pregnancy", "Breastfeeding"],
                confidence_score=0.92,
                reasoning="Retinoids are gold standard for acne treatment, increasing cell turnover",
                alternatives=["Adapalene gel for sensitive skin"]
            ))

        # Moisturizer
        products.append(ProductRecommendation(
            product_name="Lightweight Gel Moisturizer with Ceramides",
            category="moisturizer",
            key_ingredients=["ceramides", "hyaluronic_acid"],
            benefits=["Hydrates without clogging", "Repairs barrier", "Supports active treatments"],
            suitable_for=["oily", "acne-prone"],
            application_instructions="Apply AM and PM after treatments",
            frequency="Twice daily",
            contraindications=[],
            confidence_score=0.9,
            reasoning="Barrier support is essential when using acne treatments to prevent irritation",
            alternatives=None
        ))

        # Sunscreen
        products.append(ProductRecommendation(
            product_name="Oil-Free Mineral Sunscreen SPF 30+",
            category="sunscreen",
            key_ingredients=["zinc_oxide"],
            benefits=["UV protection", "Non-comedogenic", "Prevents dark spots"],
            suitable_for=["acne-prone"],
            application_instructions="Apply as last AM step, reapply every 2 hours in sun",
            frequency="Every morning",
            contraindications=[],
            confidence_score=1.0,
            reasoning="Sunscreen is crucial to prevent post-inflammatory hyperpigmentation from acne",
            alternatives=["Chemical sunscreen if mineral leaves white cast"]
        ))

        return products

    async def _generate_treatment_plan(
        self,
        analysis: AnalysisResponse,
        user_profile: Optional[Dict]
    ) -> TreatmentPlan:
        """Generate comprehensive treatment plan."""
        plan_id = f"plan_{uuid.uuid4().hex[:12]}"

        morning_routine = [
            RoutineStep(
                step_number=1,
                time_of_day="AM",
                action="Cleanse",
                products=["Gentle gel cleanser"],
                instructions="Wet face, massage cleanser for 60 seconds, rinse with lukewarm water",
                duration="1-2 minutes",
                tips=["Don't use hot water", "Pat dry gently"]
            ),
            RoutineStep(
                step_number=2,
                time_of_day="AM",
                action="Treat",
                products=["10% Niacinamide serum"],
                instructions="Apply 2-3 drops to face and neck",
                duration="1 minute",
                tips=["Wait 30 seconds before next step"]
            ),
            RoutineStep(
                step_number=3,
                time_of_day="AM",
                action="Moisturize",
                products=["Lightweight gel moisturizer"],
                instructions="Apply even layer to face and neck",
                duration="1 minute",
                tips=["Can mix with next product"]
            ),
            RoutineStep(
                step_number=4,
                time_of_day="AM",
                action="Protect",
                products=["SPF 30+ sunscreen"],
                instructions="Apply generous amount (1/4 tsp for face)",
                duration="1 minute",
                tips=["Don't skip this step!"]
            )
        ]

        evening_routine = [
            RoutineStep(
                step_number=1,
                time_of_day="PM",
                action="Cleanse",
                products=["Salicylic acid cleanser"],
                instructions="Massage on damp skin for 60 seconds, rinse",
                duration="1-2 minutes",
                tips=["Use lukewarm water"]
            ),
            RoutineStep(
                step_number=2,
                time_of_day="PM",
                action="Treat (Active)",
                products=["Retinoid cream"],
                instructions="Apply pea-sized amount to dry skin (start 2x/week)",
                duration="1 minute",
                tips=["Wait 20 min after cleansing", "Start slow!"]
            ),
            RoutineStep(
                step_number=3,
                time_of_day="PM",
                action="Hydrate",
                products=["Hyaluronic acid serum"],
                instructions="Apply to slightly damp skin",
                duration="1 minute",
                tips=["Helps reduce retinoid dryness"]
            ),
            RoutineStep(
                step_number=4,
                time_of_day="PM",
                action="Moisturize",
                products=["Barrier repair cream"],
                instructions="Apply generous layer to seal everything in",
                duration="1 minute",
                tips=["Can add extra on dry areas"]
            )
        ]

        return TreatmentPlan(
            plan_id=plan_id,
            plan_name="Acne Treatment & Prevention Plan",
            duration="12-16 weeks for full results",
            primary_goals=[
                "Reduce active breakouts",
                "Prevent new acne formation",
                "Fade post-acne marks",
                "Improve overall skin health"
            ],
            morning_routine=morning_routine,
            evening_routine=evening_routine,
            weekly_treatments=[
                RoutineStep(
                    step_number=1,
                    time_of_day="Weekly",
                    action="Deep cleanse",
                    products=["Clay mask"],
                    instructions="Apply 1-2x per week, leave for 10 min, rinse",
                    tips=["Skip on retinoid nights"]
                )
            ],
            lifestyle_recommendations=[
                "Wash pillowcases weekly",
                "Avoid touching face throughout the day",
                "Clean phone screen daily",
                "Manage stress through exercise or meditation",
                "Get 7-9 hours of sleep",
                "Stay hydrated (8 glasses water daily)"
            ],
            dietary_suggestions=[
                "Reduce high-glycemic foods (white bread, sugary snacks)",
                "Consider reducing dairy intake",
                "Increase omega-3 fatty acids (fish, walnuts, flaxseed)",
                "Eat plenty of vegetables and fruits",
                "Limit processed foods"
            ],
            expected_timeline={
                "Week 2-3": "Possible initial purging (temporary worsening)",
                "Week 4-6": "Reduction in new breakouts",
                "Week 8-10": "Noticeable improvement in texture and tone",
                "Week 12-16": "Significant improvement, clearer skin"
            },
            monitoring_metrics=[
                "Number of active breakouts",
                "Severity of inflammation",
                "Oiliness levels",
                "Skin texture",
                "Dark spot fading"
            ],
            adjustment_triggers=[
                "Excessive dryness or irritation",
                "No improvement after 8 weeks",
                "New allergic reactions",
                "Worsening after initial period"
            ]
        )

    def _extract_key_ingredients(self, analysis: AnalysisResponse) -> List[str]:
        """Extract key ingredients to use based on analysis."""
        ingredients = ["niacinamide", "salicylic_acid"]

        if analysis.severity_assessment in ["moderate", "severe"]:
            ingredients.extend(["retinoids", "benzoyl_peroxide"])

        if "inflammation" in str(analysis.biomarker_interpretation):
            ingredients.append("azelaic_acid")

        return ingredients

    def _get_ingredients_to_avoid(self, user_profile: Optional[Dict]) -> List[str]:
        """Get ingredients to avoid based on user profile."""
        avoid = ["fragrance", "essential_oils", "alcohol_denat"]

        if user_profile:
            allergies = user_profile.get("allergies", [])
            avoid.extend(allergies)

        return list(set(avoid))

    def _generate_warnings(self, key_ingredients: List[str]) -> List[str]:
        """Generate safety warnings for ingredients."""
        warnings = []

        if "retinoids" in key_ingredients:
            warnings.append("IMPORTANT: Retinoids increase sun sensitivity - SPF is mandatory")
            warnings.append("Do not use retinoids if pregnant or breastfeeding")

        if "benzoyl_peroxide" in key_ingredients:
            warnings.append("Benzoyl peroxide may bleach fabrics and hair")

        if "salicylic_acid" in key_ingredients:
            warnings.append("Avoid salicylic acid if allergic to aspirin")

        warnings.append("Patch test new products before full application")
        warnings.append("Introduce new actives one at a time, 1-2 weeks apart")

        return warnings

    def _generate_important_notes(self, analysis: AnalysisResponse) -> List[str]:
        """Generate important notes for user."""
        notes = [
            "Consistency is key - results take 8-12 weeks minimum",
            "Initial purging is normal when starting active treatments",
            "Listen to your skin - reduce frequency if too irritated"
        ]

        if analysis.requires_professional_care:
            notes.insert(0, "⚠️ IMPORTANT: Professional dermatologist consultation recommended")

        return notes

    def _extract_suggestions(self, llm_response: str) -> List[str]:
        """Extract follow-up suggestions from response."""
        return [
            "Would you like product recommendations?",
            "Should I create a detailed treatment plan?",
            "Do you have questions about specific ingredients?"
        ]

    def _extract_action_items(self, user_message: str, llm_response: str) -> List[str]:
        """Extract action items from conversation."""
        action_items = []

        if "routine" in user_message.lower():
            action_items.append("Review morning and evening routine steps")

        if "product" in user_message.lower():
            action_items.append("Research recommended products")

        return action_items

    def _check_needs_clarification(self, user_message: str) -> bool:
        """Check if user message needs clarification."""
        vague_terms = ["something", "kind of", "maybe", "not sure"]
        return any(term in user_message.lower() for term in vague_terms)

    def _generate_clarification_questions(self, user_message: str) -> List[str]:
        """Generate clarification questions."""
        return [
            "Can you describe your symptoms in more detail?",
            "How long have you been experiencing this?"
        ]

    def _get_referenced_knowledge(self, user_message: str) -> List[str]:
        """Get knowledge base sources referenced."""
        sources = []

        if "acne" in user_message.lower():
            sources.append("Acne Vulgaris condition database")

        if "ingredient" in user_message.lower():
            sources.append("Ingredient knowledge base")

        return sources
