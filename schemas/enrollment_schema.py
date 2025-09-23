from pydantic import BaseModel

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    student_id: int | None = None
    course_id: int | None = None

class EnrollmentOut(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True
