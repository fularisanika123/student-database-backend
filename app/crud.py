from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate


def create_student(db: Session, data: StudentCreate) -> Student:
    existing = db.query(Student).filter(Student.email == str(data.email)).first()
    if existing:
        raise ValueError("A student with this email already exists.")

    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def update_student(db: Session, student_id: int, data: StudentUpdate):
    student = get_student(db, student_id)
    if not student:
        return None

    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] is not None:
        existing = (
            db.query(Student)
            .filter(
                Student.email == str(update_data["email"]),
                Student.id != student_id,
            )
            .first()
        )
        if existing:
            raise ValueError("Another student already uses this email.")

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    student = get_student(db, student_id)
    if not student:
        return False
    db.delete(student)
    db.commit()
    return True


def search_students(db: Session, question: str, limit: int = 20):
    """Simple structured retrieval for the LangGraph chatbot.

    The relational SQLite database remains the source of truth for exact student data.
    Vector search is kept optional because the trainer instructions explicitly say a
    vector database should match the chosen retrieval use case.
    """
    tokens = [
        token.strip(".,?!:;()[]{}\"").lower()
        for token in question.split()
        if len(token.strip(".,?!:;()[]{}\"")) >= 3
    ]

    searchable = [
        Student.name,
        Student.college,
        Student.branch,
        Student.year,
        Student.skills,
    ]

    conditions = []
    for token in tokens:
        for field in searchable:
            conditions.append(field.ilike(f"%{token}%"))

    if not conditions:
        return get_students(db, 0, limit)

    results = db.query(Student).filter(or_(*conditions)).limit(limit).all()

    if not results:
        return get_students(db, 0, limit)

    return results
