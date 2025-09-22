from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    capacity: int

class CourseOut(CourseCreate):
    id: int

    class Config:
        orm_mode = True
