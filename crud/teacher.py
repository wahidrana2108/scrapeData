from models.teacher import Teacher
from sqlalchemy.orm import Session
from schemas.teacher_schema import TeacherCreate

def create_teacher(db: Session, teacher: TeacherCreate):
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
