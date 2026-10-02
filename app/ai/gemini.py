from google import genai

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


def generate_answer(question: str, student_context: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
You are the AI assistant for a Student Database Application System.

Answer the user's question only from the student database context below.
Do not invent student facts. If the required information is not present, say that it
is not available in the retrieved database context.

Do not reveal private credentials or API keys.

Student database context:
{student_context}

User question:
{question}

Give a concise, clear answer.
""".strip()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    answer = getattr(response, "text", None)
    if not answer:
        return "I could not generate an answer from the retrieved student data."
    return answer
