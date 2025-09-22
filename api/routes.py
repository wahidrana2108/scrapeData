from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from crud import student, teacher, course, enrollment
from schemas import student as student_schema
from schemas import teacher as teacher_schema
from schemas import course as course_schema
from schemas import enrollment as enrollment_schema

from models.scraped import ScrapedResource
import json

router = APIRouter()

@router.post("/students", response_model=student_schema.StudentOut)
def create_student(student_in: student_schema.StudentCreate, db: Session = Depends(get_db)):
    return student.create_student(db, student_in)

@router.get("/students/{id}", response_model=student_schema.StudentOut)
def get_student(id: int, db: Session = Depends(get_db)):
    result = student.get_student(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return result

@router.post("/teachers", response_model=teacher_schema.TeacherOut)
def create_teacher(teacher_in: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    return teacher.create_teacher(db, teacher_in)

@router.post("/courses", response_model=course_schema.CourseOut)
def create_course(course_in: course_schema.CourseCreate, db: Session = Depends(get_db)):
    return course.create_course(db, course_in)

@router.post("/students/{id}/enroll", response_model=enrollment_schema.EnrollmentOut)
def enroll(id: int, course_data: enrollment_schema.EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return enrollment.enroll_student(db, id, course_data.course_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/import/scraped")
def import_scraped_data(db: Session = Depends(get_db)):
    try:
        with open("samples/scraped.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            res = ScrapedResource(**item)
            db.add(res)
        db.commit()
        return {"message": f"{len(data)} items imported."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scraped_resources")
def list_scraped_resources(db: Session = Depends(get_db)):
    return db.query(ScrapedResource).all()
