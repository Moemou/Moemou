# Moemou - Breakoutlabs AI Skincare Agent

A field-specific AI agent designed to provide expert support for skincare, dermatology, and acne treatment through biomarker analysis.

## Overview

Moemou is an intelligent assistant for Breakoutlabs customers, offering:
- **Biomarker Analysis**: Analyzes skin biomarkers to identify underlying causes of acne
- **Expert Dermatology Knowledge**: Provides field-specific expertise in skincare and dermatology
- **Personalized Recommendations**: Suggests tailored treatment plans and products
- **Acne Treatment Support**: Specialized guidance for acne prevention and treatment

## Features

- 🔬 **Biomarker Analysis**: Intelligent analysis of skin health indicators
- 🧴 **Product Recommendations**: Personalized skincare product suggestions
- 📊 **Condition Assessment**: Expert evaluation of skin conditions and acne severity
- 💡 **Treatment Plans**: Customized skincare routines and treatment strategies
- 🔍 **Ingredient Analysis**: Detailed information on skincare ingredients and their effects
- 🤖 **AI-Powered Chat**: Natural language conversations with dermatology expertise

## Technology Stack

- **Backend**: FastAPI
- **LLM Integration**: OpenAI GPT-4 / Anthropic Claude
- **Knowledge Base**: JSON-based dermatology and skincare database
- **API**: RESTful endpoints for customer interactions

## Quick Start

### Prerequisites

- Python 3.9+
- API key for OpenAI or Anthropic Claude

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Moemou

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Edit `.env` file with your credentials:
```
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### Running the Application

```bash
# Start the API server
python src/main.py

# Or use uvicorn directly
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/consultations` - Start a new skincare consultation
- `POST /api/v1/analyze` - Analyze skin condition and biomarkers
- `POST /api/v1/chat` - Interactive chat with the skincare agent
- `GET /api/v1/recommendations/{user_id}` - Get personalized recommendations
- `POST /api/v1/products/search` - Search for suitable products
- `GET /api/v1/ingredients/{name}` - Get ingredient information

## Project Structure

```
Moemou/
├── src/
│   ├── agents/          # AI agent implementations
│   ├── llm/             # LLM integration layer
│   ├── knowledge/       # Skincare and dermatology knowledge base
│   ├── api/             # API endpoints and routes
│   ├── models/          # Data models
│   └── utils/           # Utility functions
├── config/              # Configuration files
├── tests/               # Test suite
└── docs/                # Documentation
```

## Usage Examples

### Analyze Skin Condition

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "user_id": "user123",
        "symptoms": ["persistent acne", "oily skin", "inflammation"],
        "biomarkers": {
            "sebum_production": "high",
            "inflammation_markers": "elevated",
            "skin_ph": 5.8
        }
    }
)

print(response.json())
```

### Get Product Recommendations

```python
response = requests.get(
    "http://localhost:8000/api/v1/recommendations/user123"
)

recommendations = response.json()
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

Proprietary - Breakoutlabs

## Support

For questions or support, contact the Breakoutlabs team.
