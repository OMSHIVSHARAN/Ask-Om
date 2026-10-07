# Ask-Om

AI-powered personal representative for Om Shivsharan. Ask questions about Om's background, skills, education, projects, and experience — the AI answers strictly from a verified candidate profile.

## Features

- Grounded AI responses using `data/candidate.json` as the single source of truth
- FastAPI backend with a `/chat` endpoint
- Pydantic validation for candidate data and API requests
- Groq LLM integration
- CORS configured for local development
- Hallucination prevention (tested)
- Swagger UI for interactive API testing
- Terminal chat CLI

## Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Pydantic v2
- Groq SDK
- python-dotenv

## API Endpoints

| Method | Path    | Description                        |
|--------|---------|-------------------------------------|
| GET    | `/`     | Health check                        |
| POST   | `/chat` | Send a message, get an AI response  |

## Local Setup

```bash
# Create and activate virtual environment
uv venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Server

```bash
uvicorn backend.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## Example

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Om."}'
```

```json
{
  "response": "Om Shivsharan is a Computer Engineering student at PDEA's College of Engineering, Manjari, affiliated with Savitribai Phule Pune University. He is expected to graduate in 2027."
}
```

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
Ask-Om/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── candidate.py
│   └── prompts.py
├── data/
│   └── candidate.json
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_hallucination.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Status

Backend API is functional. Frontend is not yet implemented.
