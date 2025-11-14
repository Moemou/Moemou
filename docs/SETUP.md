# Moemou Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment tool (venv)
- API key for OpenAI or Anthropic Claude

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Moemou
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

Required environment variables:

```env
# Choose your LLM provider
LLM_PROVIDER=openai  # or anthropic

# Add your API key
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-key-here

# Application settings (optional, has defaults)
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO
API_PORT=8000
```

### 5. Verify Installation

```bash
# Check Python version
python --version

# Verify dependencies
pip list

# Test configuration
python -c "from src.config import settings; print(f'LLM Provider: {settings.llm_provider}')"
```

## Running the Application

### Development Mode

```bash
# Run with auto-reload
python src/main.py

# Or use uvicorn directly
uvicorn src.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
# Set environment to production
export APP_ENV=production
export DEBUG=False

# Run with uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing the API

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Explore available endpoints
3. Try the "Try it out" feature for each endpoint

### Using curl

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Start Consultation:**
```bash
curl -X POST http://localhost:8000/api/v1/consultations \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "skin_type": "oily",
    "concerns": ["acne", "inflammation"],
    "age": 25
  }'
```

**Analyze Skin:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "symptoms": ["persistent acne", "oily skin", "inflammation"],
    "biomarkers": {
      "sebum_production": "high",
      "inflammation_markers": "elevated",
      "skin_ph": 5.8
    }
  }'
```

**Chat with Agent:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "What ingredients should I use for acne?"
  }'
```

### Using Python

```python
import requests

# Start consultation
response = requests.post(
    "http://localhost:8000/api/v1/consultations",
    json={
        "user_id": "user123",
        "skin_type": "oily",
        "concerns": ["acne", "inflammation"],
        "age": 25
    }
)
print(response.json())

# Analyze skin
analysis = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "user_id": "user123",
        "symptoms": ["persistent acne", "oily skin"],
        "biomarkers": {
            "sebum_production": "high",
            "inflammation_markers": "elevated",
            "skin_ph": 5.8
        }
    }
)
print(analysis.json())
```

## Troubleshooting

### Common Issues

**1. Import Errors**

```bash
# Solution: Ensure you're in the project root and virtual environment is activated
pwd  # Should show Moemou directory
which python  # Should show venv/bin/python
```

**2. API Key Errors**

```bash
# Verify API key is set
python -c "from src.config import settings; print(settings.openai_api_key[:10])"

# Check .env file exists and is not .env.example
ls -la .env
```

**3. Port Already in Use**

```bash
# Use a different port
uvicorn src.main:app --reload --port 8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**4. Module Not Found**

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific package
pip install fastapi uvicorn
```

### Logging

Check logs for detailed error information:

```bash
# Development: logs appear in console
python src/main.py

# Production: check log files
tail -f logs/moemou_*.log
```

## Development Workflow

### Project Structure Navigation

```
Moemou/
├── src/
│   ├── main.py           # Start here
│   ├── config.py         # Configuration
│   ├── agents/           # AI agent logic
│   ├── api/              # API endpoints
│   ├── llm/              # LLM integration
│   ├── knowledge/        # Knowledge base
│   ├── models/           # Data models
│   └── utils/            # Utilities
├── tests/                # Tests
├── docs/                 # Documentation
└── config/               # Config files
```

### Making Changes

1. **Edit code** in `src/` directory
2. **Hot reload** automatically picks up changes (in dev mode)
3. **Test** using `/docs` interactive API
4. **Check logs** for errors

### Adding New Features

1. **Models**: Add data models in `src/models/`
2. **Logic**: Add agent logic in `src/agents/`
3. **API**: Add endpoints in `src/api/routes.py`
4. **Knowledge**: Update JSON files in `src/knowledge/`

## Docker Setup (Optional)

### Build Docker Image

```bash
docker build -t moemou:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e LLM_PROVIDER=openai \
  moemou:latest
```

### Docker Compose

```bash
docker-compose up
```

## Next Steps

1. **Explore API Docs**: Visit http://localhost:8000/docs
2. **Read Architecture**: See `docs/ARCHITECTURE.md`
3. **Test Endpoints**: Try different API endpoints
4. **Customize Knowledge**: Edit knowledge base JSON files
5. **Integrate**: Connect your frontend application

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review documentation in `docs/`
3. Check application logs
4. Contact Breakoutlabs team
