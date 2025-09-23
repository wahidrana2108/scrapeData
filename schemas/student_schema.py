from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True
