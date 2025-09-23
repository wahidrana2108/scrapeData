from models.course import Course
from sqlalchemy.orm import Session
from schemas.course_schema import CourseCreate

def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
