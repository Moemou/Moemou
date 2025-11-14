# Moemou API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, implement appropriate authentication mechanisms.

## Endpoints

### Health & Status

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "llm_provider": "openai",
  "agent_type": "skincare_specialist"
}
```

---

### Consultations

#### POST /consultations

Start a new skincare consultation.

**Request Body:**
```json
{
  "user_id": "user123",
  "skin_type": "oily",
  "concerns": ["acne", "inflammation", "oily skin"],
  "current_products": ["salicylic acid cleanser"],
  "allergies": ["benzoyl peroxide"],
  "medical_conditions": [],
  "age": 25,
  "additional_info": "Acne mainly on jawline and forehead"
}
```

**Response:**
```json
{
  "consultation_id": "consult_abc123def456",
  "user_id": "user123",
  "status": "active",
  "message": "Consultation started successfully...",
  "next_steps": [
    "Complete skin analysis with biomarker data",
    "Receive personalized product recommendations",
    "Get a customized treatment plan"
  ],
  "created_at": "2024-01-15T10:30:00"
}
```

---

### Skin Analysis

#### POST /analyze

Analyze skin condition based on symptoms and biomarkers.

**Request Body:**
```json
{
  "user_id": "user123",
  "consultation_id": "consult_abc123",
  "symptoms": [
    "persistent acne on jawline",
    "oily skin",
    "inflammation",
    "blackheads"
  ],
  "biomarkers": {
    "sebum_production": "high",
    "inflammation_markers": "elevated",
    "skin_ph": 5.8,
    "hydration_level": "normal",
    "microbiome_balance": "imbalanced"
  },
  "duration": "6 months",
  "previous_treatments": ["benzoyl peroxide", "tea tree oil"]
}
```

**Response:**
```json
{
  "analysis_id": "analysis_xyz789",
  "user_id": "user123",
  "conditions": [
    {
      "condition_name": "Acne Vulgaris",
      "severity": "moderate",
      "confidence": 0.85,
      "description": "Chronic inflammatory skin condition...",
      "affected_areas": ["jawline", "forehead"],
      "triggers": ["excess sebum", "bacteria", "inflammation"],
      "contributing_factors": ["hormonal", "microbiome imbalance"]
    }
  ],
  "primary_diagnosis": "Acne Vulgaris",
  "biomarker_interpretation": {
    "sebum_production": "Indicates overactive sebaceous glands...",
    "inflammation_markers": "Suggests inflammatory acne type...",
    "skin_ph": "Alkaline - Compromised barrier, acne risk"
  },
  "root_causes": [
    "Excess sebum production",
    "Bacterial overgrowth",
    "Inflammation"
  ],
  "severity_assessment": "moderate",
  "recommendations_preview": [
    "Use gentle, pH-balanced cleanser",
    "Incorporate niacinamide for oil control",
    "Apply salicylic acid for exfoliation"
  ],
  "requires_professional_care": false,
  "confidence_score": 0.85,
  "analysis_summary": "Based on the biomarkers and symptoms...",
  "timestamp": "2024-01-15T10:35:00"
}
```

---

### Recommendations

#### POST /recommendations

Get personalized product recommendations and treatment plan.

**Request Body:**
```json
{
  "analysis_id": "analysis_xyz789",
  "user_id": "user123",
  "conditions": [...],
  "primary_diagnosis": "Acne Vulgaris",
  "biomarker_interpretation": {...},
  "root_causes": [...],
  "severity_assessment": "moderate",
  "user_profile": {
    "allergies": ["benzoyl peroxide"],
    "budget": "moderate",
    "preferences": {
      "natural": false,
      "fragrance_free": true
    }
  }
}
```

**Response:**
```json
{
  "recommendation_id": "rec_mno345",
  "user_id": "user123",
  "products": [
    {
      "product_name": "Gentle Salicylic Acid Cleanser",
      "category": "cleanser",
      "key_ingredients": ["salicylic_acid", "niacinamide"],
      "benefits": ["Unclogs pores", "Reduces oil"],
      "suitable_for": ["oily", "acne-prone"],
      "application_instructions": "Use AM and PM...",
      "frequency": "Twice daily",
      "contraindications": ["Aspirin allergy"],
      "confidence_score": 0.9,
      "reasoning": "Salicylic acid is essential...",
      "alternatives": ["Gentle cream cleanser"]
    }
  ],
  "treatment_plan": {
    "plan_id": "plan_pqr678",
    "plan_name": "Acne Treatment & Prevention Plan",
    "duration": "12-16 weeks",
    "primary_goals": ["Reduce breakouts", "Prevent new acne"],
    "morning_routine": [...],
    "evening_routine": [...],
    "lifestyle_recommendations": [...],
    "expected_timeline": {...}
  },
  "key_ingredients_to_use": [
    "niacinamide",
    "salicylic_acid",
    "retinoids"
  ],
  "ingredients_to_avoid": [
    "benzoyl_peroxide",
    "fragrance",
    "alcohol_denat"
  ],
  "timeline": "4-8 weeks for initial improvement",
  "expected_results": "Reduction in new breakouts...",
  "follow_up_schedule": [
    "Week 2: Check for reactions",
    "Week 4: Assess initial response"
  ],
  "warnings": [
    "IMPORTANT: Retinoids increase sun sensitivity",
    "Patch test new products"
  ],
  "important_notes": [
    "Consistency is key",
    "Results take 8-12 weeks"
  ],
  "timestamp": "2024-01-15T10:40:00"
}
```

---

### Chat

#### POST /chat

Interactive chat with the skincare agent.

**Request Body:**
```json
{
  "user_id": "user123",
  "message": "What's the difference between salicylic acid and glycolic acid?",
  "consultation_id": "consult_abc123",
  "conversation_history": [
    {
      "role": "user",
      "content": "I have oily, acne-prone skin",
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "role": "assistant",
      "content": "For oily, acne-prone skin...",
      "timestamp": "2024-01-15T10:30:05"
    }
  ],
  "include_analysis": false
}
```

**Response:**
```json
{
  "response": "Great question! Salicylic acid and glycolic acid are both exfoliants...",
  "conversation_id": "chat_stu901",
  "suggestions": [
    "Would you like product recommendations?",
    "Should I create a detailed treatment plan?"
  ],
  "action_items": [
    "Review morning and evening routine steps"
  ],
  "referenced_knowledge": [
    "Ingredient knowledge base"
  ],
  "confidence": 0.9,
  "requires_clarification": false,
  "clarification_questions": null,
  "timestamp": "2024-01-15T10:45:00"
}
```

---

### Knowledge Base

#### GET /ingredients/{ingredient_name}

Get detailed information about a specific ingredient.

**Example:** `/ingredients/niacinamide`

**Response:**
```json
{
  "ingredient_name": "niacinamide",
  "data": {
    "name": "Niacinamide (Vitamin B3)",
    "category": "Vitamin",
    "description": "Multi-functional ingredient...",
    "benefits": [
      "Reduces sebum production",
      "Minimizes pore appearance"
    ],
    "addresses": ["acne", "hyperpigmentation"],
    "concentration_range": "2% - 10%",
    "suitable_for": ["all skin types"],
    "synergistic_with": ["hyaluronic_acid", "ceramides"]
  }
}
```

#### GET /conditions/{condition_name}

Get detailed information about a skin condition.

**Example:** `/conditions/acne`

**Response:**
```json
{
  "condition_name": "acne",
  "data": {
    "name": "Acne Vulgaris",
    "description": "Chronic inflammatory skin condition...",
    "types": {
      "comedonal": {...},
      "inflammatory": {...},
      "cystic": {...}
    },
    "root_causes": [...],
    "recommended_ingredients": [...],
    "treatments": [...]
  }
}
```

---

### Product Search

#### GET /products/search

Search for products by category or concern.

**Query Parameters:**
- `category` (optional): Product category (e.g., "cleanser", "moisturizer")
- `concern` (optional): Skin concern (e.g., "acne", "aging")

**Example:** `/products/search?concern=acne`

**Response:**
```json
{
  "query_type": "concern",
  "query": "acne",
  "recommended_ingredients": [
    {
      "name": "salicylic_acid",
      "benefits": ["Unclogs pores", "Reduces blackheads"],
      "addresses": ["acne", "blackheads", "oily skin"]
    },
    {
      "name": "niacinamide",
      "benefits": ["Reduces sebum", "Anti-inflammatory"],
      "addresses": ["acne", "oily skin"]
    }
  ]
}
```

---

### Biomarker Analysis

#### POST /analyze-biomarkers

Analyze biomarker data and provide interpretation.

**Request Body:**
```json
{
  "biomarkers": {
    "sebum_production": "high",
    "inflammation_markers": "elevated",
    "skin_ph": 5.8,
    "hydration_level": "normal"
  },
  "skin_type": "oily",
  "concerns": ["acne", "inflammation"],
  "age": 25
}
```

**Response:**
```json
{
  "biomarkers": {...},
  "interpretation": {
    "sebum_production": "Indicates overactive sebaceous glands...",
    "inflammation_markers": "Suggests inflammatory acne type...",
    "skin_ph": "Alkaline - Compromised barrier, acne risk"
  },
  "skin_type": "oily",
  "concerns": ["acne", "inflammation"],
  "recommendations": [
    "Use products targeting identified imbalances",
    "Monitor biomarkers regularly"
  ]
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production.

## Data Privacy

- User data is not persisted by default
- Implement appropriate data privacy measures for production
- Follow GDPR and other relevant regulations
- Add medical disclaimers where appropriate

## Interactive Documentation

Visit `/docs` for interactive API documentation where you can test endpoints directly.
