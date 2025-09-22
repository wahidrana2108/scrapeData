from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from models.base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
    )
