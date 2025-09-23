from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    description: str | None = None
    capacity: int | None = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    capacity: int | None = None

class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True
