from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.gemini import generate_answer
from app.crud import search_students
from app.database import SessionLocal


class ChatState(TypedDict):
    question: str
    student_context: str
    answer: str
    records_used: int


def retrieve_student_data(state: ChatState):
    db = SessionLocal()
    try:
        students = search_students(db, state["question"], limit=20)
        lines = []

        # The chatbot context intentionally omits email/phone to reduce unnecessary
        # exposure of contact information. CRUD APIs still manage those fields.
        for student in students:
            lines.append(
                f"ID: {student.id}; Name: {student.name}; "
                f"College: {student.college or 'N/A'}; Branch: {student.branch}; "
                f"Year: {student.year}; Skills: {student.skills or 'N/A'}"
            )

        context = "\n".join(lines) if lines else "No student records found."
        return {
            "student_context": context,
            "records_used": len(students),
        }
    finally:
        db.close()


def generate_gemini_answer(state: ChatState):
    answer = generate_answer(state["question"], state["student_context"])
    return {"answer": answer}


graph_builder = StateGraph(ChatState)
graph_builder.add_node("retrieve_student_data", retrieve_student_data)
graph_builder.add_node("generate_gemini_answer", generate_gemini_answer)
graph_builder.add_edge(START, "retrieve_student_data")
graph_builder.add_edge("retrieve_student_data", "generate_gemini_answer")
graph_builder.add_edge("generate_gemini_answer", END)
chatbot_graph = graph_builder.compile()


def ask_chatbot(question: str):
    return chatbot_graph.invoke(
        {
            "question": question,
            "student_context": "",
            "answer": "",
            "records_used": 0,
        }
    )
