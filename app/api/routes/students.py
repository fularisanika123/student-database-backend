from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import StudentCreate, StudentRead, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Student email must be unique.") from exc


@router.get("/", response_model=list[StudentRead])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0:
        raise HTTPException(status_code=400, detail="skip cannot be negative")
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")
    return crud.get_students(db, skip, limit)


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    try:
        student = crud.update_student(db, student_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return None
