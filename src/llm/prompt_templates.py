"""
Prompt templates for the Breakoutlabs skincare agent.
Contains specialized prompts for dermatology, biomarker analysis, and acne treatment.
"""

from typing import Dict, List, Optional


class PromptTemplates:
    """Collection of prompt templates for the skincare AI agent."""

    SYSTEM_PROMPT = """You are an expert dermatology and skincare AI assistant for Breakoutlabs,
specializing in acne treatment and biomarker analysis. Your role is to provide scientifically-backed,
personalized skincare guidance to help customers achieve clear, healthy skin.

Your expertise includes:
- Dermatological conditions, especially acne and related skin concerns
- Biomarker interpretation for skin health assessment
- Skincare ingredient analysis and product recommendations
- Evidence-based treatment protocols
- Personalized routine development

Guidelines:
1. Always prioritize safety and recommend professional medical consultation for severe conditions
2. Base recommendations on scientific evidence and dermatological best practices
3. Consider individual factors: skin type, biomarkers, allergies, and medical history
4. Provide clear, actionable advice with specific product categories and ingredients
5. Explain the 'why' behind recommendations to educate users
6. Be honest about treatment timelines and realistic expectations
7. Flag any concerning symptoms that require professional medical attention

Remember: You are a supportive expert helping people achieve their skincare goals through
personalized, science-based guidance."""

    BIOMARKER_ANALYSIS_PROMPT = """Analyze the following biomarker data for skin health assessment:

{biomarker_data}

User Context:
- Skin Type: {skin_type}
- Primary Concerns: {concerns}
- Age: {age}

Based on these biomarkers, provide:
1. Interpretation of each biomarker and what it indicates about skin health
2. Identification of root causes for any skin issues
3. Key imbalances or deficiencies that need addressing
4. How these biomarkers relate to acne and skin inflammation
5. Specific recommendations to optimize these markers

Be precise, scientific, and actionable in your analysis."""

    SKIN_ANALYSIS_PROMPT = """Perform a comprehensive skin analysis based on the following information:

Symptoms: {symptoms}
Duration: {duration}
Previous Treatments: {previous_treatments}
Biomarkers: {biomarkers}

Provide a detailed analysis including:
1. Primary diagnosis and condition identification
2. Severity assessment (mild, moderate, severe)
3. Root causes and contributing factors
4. Potential triggers to avoid
5. Whether professional dermatological care is recommended
6. Confidence level in the assessment

Be thorough but concise, focusing on actionable insights."""

    PRODUCT_RECOMMENDATION_PROMPT = """Based on the following profile, recommend specific skincare products and ingredients:

Skin Analysis: {skin_analysis}
Biomarker Summary: {biomarker_summary}
User Preferences: {user_preferences}
Allergies/Sensitivities: {allergies}
Budget Constraints: {budget}

Provide recommendations for:
1. Essential products (cleanser, treatment, moisturizer)
2. Key active ingredients to look for
3. Ingredients to avoid
4. Product categories in order of priority
5. Application frequency and instructions
6. Expected timeline for results

Focus on efficacy, safety, and compatibility with the user's unique skin profile."""

    TREATMENT_PLAN_PROMPT = """Create a comprehensive, personalized acne treatment plan:

Diagnosis: {diagnosis}
Severity: {severity}
Biomarkers: {biomarkers}
User Profile: {user_profile}

Develop a structured plan including:
1. Morning routine (step-by-step)
2. Evening routine (step-by-step)
3. Weekly/monthly treatments
4. Lifestyle and dietary recommendations
5. Timeline and expected milestones
6. Monitoring metrics to track progress
7. When to adjust the plan

Make it practical, sustainable, and evidence-based."""

    CHAT_RESPONSE_PROMPT = """You are chatting with a Breakoutlabs customer seeking skincare advice.

Conversation Context: {conversation_history}
User Question: {user_message}
User Profile: {user_profile}

Respond naturally and helpfully:
1. Answer their specific question
2. Provide relevant context and education
3. Suggest next steps or follow-up actions
4. Offer related insights that might be helpful
5. Ask clarifying questions if needed

Keep responses conversational but professional, empathetic but scientific."""

    INGREDIENT_ANALYSIS_PROMPT = """Analyze the following skincare ingredient for a user with this profile:

Ingredient: {ingredient_name}
User Skin Type: {skin_type}
Concerns: {concerns}
Current Routine: {current_routine}
Allergies: {allergies}

Provide:
1. What this ingredient does and how it works
2. Benefits for their specific skin concerns
3. Potential side effects or considerations
4. How to incorporate it into their routine
5. Interactions with other ingredients they're using
6. Recommended concentration and frequency
7. Whether it's suitable for their profile

Be educational and specific."""

    @staticmethod
    def format_biomarker_analysis(
        biomarker_data: Dict,
        skin_type: Optional[str] = None,
        concerns: Optional[List[str]] = None,
        age: Optional[int] = None
    ) -> str:
        """Format the biomarker analysis prompt with user data."""
        return PromptTemplates.BIOMARKER_ANALYSIS_PROMPT.format(
            biomarker_data=str(biomarker_data),
            skin_type=skin_type or "Not specified",
            concerns=", ".join(concerns) if concerns else "Not specified",
            age=age or "Not specified"
        )

    @staticmethod
    def format_skin_analysis(
        symptoms: List[str],
        duration: Optional[str] = None,
        previous_treatments: Optional[List[str]] = None,
        biomarkers: Optional[Dict] = None
    ) -> str:
        """Format the skin analysis prompt."""
        return PromptTemplates.SKIN_ANALYSIS_PROMPT.format(
            symptoms=", ".join(symptoms),
            duration=duration or "Not specified",
            previous_treatments=", ".join(previous_treatments) if previous_treatments else "None",
            biomarkers=str(biomarkers) if biomarkers else "Not available"
        )

    @staticmethod
    def format_product_recommendation(
        skin_analysis: str,
        biomarker_summary: str,
        user_preferences: Optional[Dict] = None,
        allergies: Optional[List[str]] = None,
        budget: Optional[str] = None
    ) -> str:
        """Format the product recommendation prompt."""
        return PromptTemplates.PRODUCT_RECOMMENDATION_PROMPT.format(
            skin_analysis=skin_analysis,
            biomarker_summary=biomarker_summary,
            user_preferences=str(user_preferences) if user_preferences else "None specified",
            allergies=", ".join(allergies) if allergies else "None",
            budget=budget or "Not specified"
        )

    @staticmethod
    def format_treatment_plan(
        diagnosis: str,
        severity: str,
        biomarkers: Optional[Dict] = None,
        user_profile: Optional[Dict] = None
    ) -> str:
        """Format the treatment plan prompt."""
        return PromptTemplates.TREATMENT_PLAN_PROMPT.format(
            diagnosis=diagnosis,
            severity=severity,
            biomarkers=str(biomarkers) if biomarkers else "Not available",
            user_profile=str(user_profile) if user_profile else "Limited information"
        )

    @staticmethod
    def format_chat_response(
        conversation_history: List[Dict],
        user_message: str,
        user_profile: Optional[Dict] = None
    ) -> str:
        """Format the chat response prompt."""
        history_str = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history[-5:]  # Last 5 messages for context
        ])
        return PromptTemplates.CHAT_RESPONSE_PROMPT.format(
            conversation_history=history_str if history_str else "No previous context",
            user_message=user_message,
            user_profile=str(user_profile) if user_profile else "New user"
        )
