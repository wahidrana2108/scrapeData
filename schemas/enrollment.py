from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentOut(EnrollmentCreate):
    id: int

    class Config:
        orm_mode = True

