from sqlalchemy import Column, Integer, String

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    college = Column(String(150), nullable=True)
    branch = Column(String(100), nullable=False)
    year = Column(String(20), nullable=False)
    skills = Column(String(500), nullable=True)
