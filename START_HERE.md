# START HERE — Student Database Application System

This is the complete baseline project. Follow the numbered steps in order.
You should not rewrite earlier files when moving to a later step; the project
structure and code are already prepared for all required components.

## Step 1 — Open the project

Open this folder in VS Code:

`student-database-backend-v1`

## Step 2 — Create virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Step 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

If ChromaDB cannot be installed with your local Python version, use Python 3.13
for the virtual environment and keep the same project files.

## Step 4 — Create Gemini API key

Open Google AI Studio and use the API Keys page. Create/copy a key.

Official guide:
https://ai.google.dev/gemini-api/docs/get-started

## Step 5 — Create `.env`

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env`.

## Step 6 — Create sample student data

```powershell
python seed_data.py
```

## Step 7 — Run FastAPI

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Step 8 — Test CRUD in Swagger

Use these endpoints:

```text
POST   /students/
GET    /students/
GET    /students/{student_id}
PUT    /students/{student_id}
DELETE /students/{student_id}
```

## Step 9 — Test the LangGraph + Gemini chatbot

Use:

`POST /chatbot/ask`

Example:

```json
{
  "question": "Which students know Python?"
}
```

The workflow is:

```text
Question -> LangGraph -> SQLite student retrieval -> Gemini -> Answer
```

## Step 10 — Vector database requirement

Read `VECTOR_DB_RESEARCH.md`.
ChromaDB is selected as an optional semantic-retrieval layer. SQLite remains the
source of truth for structured CRUD.

## Step 11 — Deployment setup

A Dockerfile is included.

```powershell
docker build -t student-db-backend .
docker run --env-file .env -p 8000:8000 student-db-backend
```

## Step 12 — Final test

```powershell
pytest
```

Also manually test the CRUD endpoints, Swagger, and chatbot flow.

## Step 13 — GitHub

```powershell
git init
git add .
git status
git commit -m "Student Database Backend project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Before pushing, confirm that `.env` and `students.db` are not committed.

## Step 14 — Submission

Open the Google Form provided by management and submit the accessible GitHub
repository URL before the company deadline.
