from sqlalchemy.orm import Session
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course
from schemas.enrollment_schema import EnrollmentCreate
from fastapi import HTTPException, status


def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    # 1. Student exists কিনা চেক
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {enrollment.student_id} not found",
        )

    # 2. if Course exists
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {enrollment.course_id} not found",
        )

    # 3. Duplicate enrollment check
    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == enrollment.course_id,
        )
        .first()
    )
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course",
        )

    # 4. Course capacity check
    enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
    if enrolled_count >= course.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course capacity has been reached",
        )

    # 5. if every thing is ok then enrollment
    db_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def get_enrollment(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Enrollment).offset(skip).limit(limit).all()


def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
        return True
    return False
