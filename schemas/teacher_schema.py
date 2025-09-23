from pydantic import BaseModel

class TeacherBase(BaseModel):
    name: str
    email: str

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class TeacherOut(TeacherBase):
    id: int

    class Config:
        from_attributes = True
