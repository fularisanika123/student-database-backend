from fastapi import FastAPI
from fastapi.responses import FileResponse, Response

from app import models
from app.api.routes.chatbot import router as chatbot_router
from app.api.routes.students import router as students_router
from app.core.config import APP_NAME
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description=(
        "Modular FastAPI backend for student CRUD, Swagger documentation, "
        "Gemini, and a LangGraph chatbot."
    ),
    version="1.0.0",
)

app.include_router(students_router)
app.include_router(chatbot_router)


@app.get("/", tags=["Frontend"])
def home():
    return FileResponse("index.html")


@app.get("/style.css", include_in_schema=False)
def style():
    return FileResponse("style.css", media_type="text/css")


@app.get("/script.js", include_in_schema=False)
def script():
    return FileResponse("script.js", media_type="application/javascript")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}