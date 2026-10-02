from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    college: str | None = Field(default=None, max_length=150)
    branch: str = Field(min_length=2, max_length=100)
    year: str = Field(min_length=1, max_length=20)
    skills: str | None = Field(default=None, max_length=500)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    college: str | None = Field(default=None, max_length=150)
    branch: str | None = Field(default=None, min_length=2, max_length=100)
    year: str | None = Field(default=None, min_length=1, max_length=20)
    skills: str | None = Field(default=None, max_length=500)


class StudentRead(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class ChatResponse(BaseModel):
    question: str
    answer: str
    records_used: int
