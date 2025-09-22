from sqlalchemy.orm import Session
from models.enrollment import Enrollment
from models.course import Course
from sqlalchemy.exc import IntegrityError

def enroll_student(db: Session, student_id: int, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    count = db.query(Enrollment).filter(Enrollment.course_id == course_id).count()

    if not course or count >= course.capacity:
        raise ValueError("Course is full or doesn't exist.")

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    try:
        db.commit()
        db.refresh(enrollment)
        return enrollment
    except IntegrityError:
        db.rollback()
        raise ValueError("Duplicate enrollment not allowed.")
