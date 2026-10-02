# Student Database Application System – Backend

## Project Overview

A modular backend for managing student information through FastAPI CRUD APIs, with
Swagger/OpenAPI documentation and an AI chatbot using Gemini and LangGraph.

## Required Features Covered

- Modular backend architecture
- Student database schema
- CRUD APIs
- Input validation and HTTP error handling
- FastAPI Swagger/OpenAPI documentation
- Gemini API integration
- LangGraph chatbot workflow
- Student-data retrieval through the chatbot
- Vector database research and selection
- Dockerfile for deployable backend setup
- README and setup documentation

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini API (`google-genai`)
- LangGraph
- ChromaDB (optional semantic retrieval layer)
- Docker
- Git/GitHub

## Project Structure

```text
student-database-backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── api/routes/
│   │   ├── students.py
│   │   └── chatbot.py
│   ├── ai/
│   │   ├── gemini.py
│   │   ├── langgraph_agent.py
│   │   └── vector_db.py
│   └── core/config.py
├── tests/test_api.py
├── seed_data.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── VECTOR_DB_RESEARCH.md
```

## 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure Gemini

Create a `.env` file by copying `.env.example` and put your Gemini API key in:

```text
GEMINI_API_KEY=YOUR_KEY
```

Never commit `.env` to GitHub.

## 4. Seed demo data

```powershell
python seed_data.py
```

## 5. Run the backend

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## 6. API Endpoints

### Student CRUD

```text
POST   /students/
GET    /students/
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}
```

### AI Chatbot

```text
POST /chatbot/ask
```

Example request:

```json
{
  "question": "Which students know Python?"
}
```

## 7. Chatbot Flow

```text
User question
      ↓
LangGraph workflow
      ↓
Retrieve relevant student data from SQLite
      ↓
Gemini generates the natural-language response
      ↓
Return response to user
```

The chatbot context intentionally excludes phone numbers and emails to reduce
unnecessary exposure of contact information.

## 8. Vector Database

See `VECTOR_DB_RESEARCH.md`. ChromaDB is selected for an optional semantic-retrieval
layer while SQLite remains the source of truth for structured CRUD operations.

## 9. Docker

Build:

```powershell
docker build -t student-db-backend .
```

Run:

```powershell
docker run --env-file .env -p 8000:8000 student-db-backend
```

## 10. Testing

Run:

```powershell
pytest
```

## 11. GitHub Safety Checklist

Before pushing:

- `.env` is not committed.
- No Gemini API key is present in source files.
- README is present.
- `requirements.txt` is present.
- The application can be started with Uvicorn.
- Swagger `/docs` opens successfully.
