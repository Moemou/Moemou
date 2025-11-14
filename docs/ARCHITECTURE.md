# Moemou Architecture

## Overview

Moemou is a field-specific AI agent designed for Breakoutlabs to provide expert skincare, dermatology, and acne treatment support. The system combines LLM capabilities with a curated knowledge base to deliver personalized, scientifically-backed recommendations.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
│              (FastAPI - RESTful Endpoints)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    Skincare Agent                            │
│           (Core AI Logic & Orchestration)                    │
└─────────┬──────────────────────────────┬────────────────────┘
          │                              │
          ↓                              ↓
┌──────────────────────┐      ┌──────────────────────┐
│   LLM Integration    │      │   Knowledge Base     │
│   (OpenAI/Claude)    │      │   (JSON Database)    │
│                      │      │                      │
│ - Client Interface   │      │ - Conditions         │
│ - Prompt Templates   │      │ - Ingredients        │
│ - Response Parsing   │      │ - Products           │
└──────────────────────┘      │ - Biomarkers         │
                              └──────────────────────┘
```

## Components

### 1. API Layer (`src/api/`)

**Purpose**: Expose skincare agent functionality through RESTful endpoints

**Key Files**:
- `routes.py`: API endpoint definitions
- FastAPI application with dependency injection

**Endpoints**:
- `POST /api/v1/consultations` - Start new consultation
- `POST /api/v1/analyze` - Analyze skin condition
- `POST /api/v1/recommendations` - Get personalized recommendations
- `POST /api/v1/chat` - Interactive chat
- `GET /api/v1/ingredients/{name}` - Ingredient information
- `GET /api/v1/conditions/{name}` - Condition information

### 2. Skincare Agent (`src/agents/`)

**Purpose**: Core AI agent with dermatology expertise

**Key Class**: `SkincareAgent`

**Responsibilities**:
1. **Skin Analysis**: Analyze symptoms and biomarkers to identify conditions
2. **Biomarker Interpretation**: Interpret skin health metrics
3. **Product Recommendations**: Generate personalized product suggestions
4. **Treatment Planning**: Create comprehensive skincare routines
5. **Chat Interactions**: Conversational support and guidance

**Key Methods**:
- `analyze_skin()`: Comprehensive skin analysis
- `generate_recommendations()`: Product and treatment recommendations
- `chat()`: Conversational interactions
- `_interpret_biomarkers()`: Biomarker analysis

### 3. LLM Integration (`src/llm/`)

**Purpose**: Unified interface for different LLM providers

**Components**:
- `LLMClient`: Abstract base class
- `OpenAIClient`: OpenAI integration
- `AnthropicClient`: Anthropic Claude integration
- `PromptTemplates`: Specialized prompts for dermatology

**Features**:
- Provider-agnostic interface
- Streaming support
- Temperature and token configuration
- Specialized dermatology prompts

### 4. Knowledge Base (`src/knowledge/`)

**Purpose**: Curated dermatology and skincare knowledge

**Data Files**:
- `conditions.json`: Skin conditions, types, treatments
- `ingredients.json`: Active ingredients, benefits, contraindications
- `products.json`: Product categories and recommendations
- `biomarkers.json`: Biomarker interpretations and implications

**Loader**: `KnowledgeBase` class for querying knowledge

### 5. Data Models (`src/models/`)

**Purpose**: Type-safe data structures using Pydantic

**Models**:
- `Consultation`, `ConsultationRequest`, `ConsultationResponse`
- `AnalysisRequest`, `AnalysisResponse`, `Biomarkers`, `SkinCondition`
- `ProductRecommendation`, `TreatmentPlan`, `RoutineStep`
- `ChatMessage`, `ChatRequest`, `ChatResponse`

### 6. Configuration (`src/config.py`)

**Purpose**: Centralized configuration management

**Features**:
- Environment variable loading
- LLM provider configuration
- API settings
- Feature flags

## Data Flow

### Skin Analysis Flow

```
User Request (symptoms, biomarkers)
        ↓
API Endpoint (/analyze)
        ↓
SkincareAgent.analyze_skin()
        ↓
    ┌───┴────┐
    ↓        ↓
Biomarker  LLM Analysis
Analysis   (via prompts)
    ↓        ↓
    └───┬────┘
        ↓
Knowledge Base Lookup
(conditions, treatments)
        ↓
AnalysisResponse
(diagnosis, severity, recommendations)
```

### Recommendation Flow

```
Analysis Result
        ↓
SkincareAgent.generate_recommendations()
        ↓
    ┌───┴────────┐
    ↓            ↓
Knowledge Base  LLM Prompting
(ingredients,   (personalization)
 products)
    ↓            ↓
    └─────┬──────┘
          ↓
Product Selection
Treatment Plan Generation
          ↓
RecommendationResponse
(products, routine, timeline)
```

## AI Agent Design

### Hybrid Approach

The agent combines two complementary approaches:

1. **Knowledge-Based**: Structured data from curated knowledge base
2. **LLM-Powered**: Natural language understanding and generation

This hybrid approach ensures:
- Accuracy through validated knowledge
- Flexibility through LLM reasoning
- Personalization through context understanding

### Prompt Engineering

Specialized prompts for each use case:
- `SYSTEM_PROMPT`: Core dermatology expertise
- `BIOMARKER_ANALYSIS_PROMPT`: Biomarker interpretation
- `SKIN_ANALYSIS_PROMPT`: Condition diagnosis
- `PRODUCT_RECOMMENDATION_PROMPT`: Product selection
- `TREATMENT_PLAN_PROMPT`: Routine creation

### Safety Measures

1. **Professional Care Flags**: Identifies severe cases requiring medical attention
2. **Contraindication Checking**: Warns about ingredient interactions
3. **Confidence Scoring**: Indicates certainty in recommendations
4. **Evidence-Based**: Recommendations based on dermatological science

## Configuration

### LLM Providers

Support for multiple providers:
- **OpenAI**: GPT-4, GPT-4 Turbo
- **Anthropic**: Claude 3 Opus, Sonnet

Configured via environment variables:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4-turbo-preview
```

### Feature Flags

- `ENABLE_BIOMARKER_ANALYSIS`: Toggle biomarker features
- `ENABLE_PRODUCT_RECOMMENDATIONS`: Toggle product recommendations
- `ENABLE_ROUTINE_BUILDER`: Toggle treatment plan generation

## Extensibility

### Adding New Conditions

1. Add condition data to `src/knowledge/conditions.json`
2. Update detection logic in `SkincareAgent._identify_conditions()`
3. Add specialized prompts if needed

### Adding New Ingredients

1. Add ingredient data to `src/knowledge/ingredients.json`
2. Knowledge base will automatically index it
3. Update recommendation logic if special handling needed

### Adding New Biomarkers

1. Add biomarker data to `src/knowledge/biomarkers.json`
2. Update `Biomarkers` model in `src/models/analysis.py`
3. Add interpretation logic in `SkincareAgent._interpret_biomarkers()`

### Supporting New LLM Providers

1. Create new client class implementing `LLMClient` interface
2. Add provider configuration in `src/config.py`
3. Update `get_llm_client()` factory function

## Security Considerations

1. **API Keys**: Never commit API keys, use environment variables
2. **Input Validation**: Pydantic models validate all inputs
3. **Rate Limiting**: Consider adding rate limiting in production
4. **User Data**: Implement proper data privacy and storage policies
5. **Medical Disclaimers**: Always include appropriate medical disclaimers

## Performance

### Optimization Strategies

1. **Knowledge Base**: JSON files loaded into memory for fast access
2. **Caching**: Consider caching LLM responses for common queries
3. **Async/Await**: Fully async architecture for concurrency
4. **Streaming**: Support for streaming LLM responses

### Scalability

- Stateless design allows horizontal scaling
- Consider database for user data persistence
- Implement caching layer (Redis) for production
- Load balancing for multiple instances

## Future Enhancements

1. **Image Analysis**: Integrate computer vision for skin photos
2. **User Profiles**: Persistent user data and history
3. **Progress Tracking**: Monitor treatment effectiveness over time
4. **Vector Database**: Semantic search over knowledge base
5. **Multi-language**: Support for multiple languages
6. **Mobile App**: Native mobile applications
