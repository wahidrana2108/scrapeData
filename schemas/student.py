from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True
