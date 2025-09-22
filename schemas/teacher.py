from pydantic import BaseModel, EmailStr

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr

class TeacherOut(TeacherCreate):
    id: int

    class Config:
        orm_mode = True
