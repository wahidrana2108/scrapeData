from typing import List

# Models
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrollment import Enrollment

# Schemas
from schemas import student_schema, teacher_schema, course_schema, enrollment_schema
from schemas.scraped_schema import ScrapedResourceBase

import json
from pathlib import Path
from models.scraped import ScrapedResource
from fastapi import APIRouter, Depends, HTTPException, status
from db import get_db
from schemas.course_schema import CourseCreate, CourseOut
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import course_schema


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.enrollment import Enrollment
from models.course import Course
from schemas import enrollment_schema


router = APIRouter()

# ---------------- Students ----------------
@router.post("/students", response_model=student_schema.StudentOut)
def create_student(student: student_schema.StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students", response_model=list[student_schema.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/students/{student_id}", response_model=student_schema.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=student_schema.StudentOut)
def update_student(student_id: int, student: student_schema.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"detail": "Student deleted"}


# ---------------- Teachers ----------------
@router.post("/teachers", response_model=teacher_schema.TeacherOut)
def create_teacher(teacher: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teachers", response_model=list[teacher_schema.TeacherOut])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()

@router.get("/teachers/{teacher_id}", response_model=teacher_schema.TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.put("/teachers/{teacher_id}", response_model=teacher_schema.TeacherOut)
def update_teacher(teacher_id: int, teacher: teacher_schema.TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in teacher.dict(exclude_unset=True).items():
        setattr(db_teacher, key, value)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"detail": "Teacher deleted"}


# ---------------- Courses ----------------
# Create Course
@router.post("/courses", response_model=course_schema.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: course_schema.CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        description=course.description,
        capacity=course.capacity
    )
    try:
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course creation failed: duplicate or invalid data")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Get all courses
@router.get("/courses", response_model=list[course_schema.CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# Get course by ID
@router.get("/courses/{course_id}", response_model=course_schema.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

# Update course
@router.put("/courses/{course_id}", response_model=course_schema.CourseOut)
def update_course(course_id: int, course: course_schema.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    for field, value in course.dict(exclude_unset=True).items():
        setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course

# Delete course
@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}


# ---------------- Enrollments ----------------
@router.post("/enrollments", response_model=enrollment_schema.EnrollmentOut)
def create_enrollment(enrollment: enrollment_schema.EnrollmentCreate, db: Session = Depends(get_db)):
    # 1. Prevent duplicate enrollment
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    # 2. Enforce course capacity
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course.capacity is not None:
        enrolled_count = db.query(Enrollment).filter(Enrollment.course_id == course.id).count()
        if enrolled_count >= course.capacity:
            raise HTTPException(status_code=400, detail="Course capacity has been reached")

    # Create new enrollment
    db_enrollment = Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


@router.get("/enrollments/{enrollment_id}", response_model=enrollment_schema.EnrollmentOut)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.put("/enrollments/{enrollment_id}", response_model=enrollment_schema.EnrollmentOut)
def update_enrollment(enrollment_id: int, enrollment: enrollment_schema.EnrollmentCreate, db: Session = Depends(get_db)):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    for key, value in enrollment.dict(exclude_unset=True).items():
        setattr(db_enrollment, key, value)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(db_enrollment)
    db.commit()
    return {"detail": "Enrollment deleted"}


# ------------------ Scraped Resources ------------------
@router.get("/scraped_resources")
def get_scraped_resources(db: Session = Depends(get_db)):
    return db.query(ScrapedResource).all()

@router.post("/import/scraped")
def import_scraped_data(db: Session = Depends(get_db)):
    import json
    from pathlib import Path

    file_path = Path("samples/scraped.json")

    if not file_path.exists():
        return {"error": "samples/scraped.json not found"}

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        return {"error": "Invalid JSON format, expected a list"}

    for item in data:
        # converting price in to float value
        price_value = item.get("price")
        try:
            price_value = float(price_value) if price_value is not None else None
        except ValueError:
            price_value = None  # if invalid then save NULL

        db_obj = ScrapedResource(
            title=item.get("title"),
            url=item.get("url"),
            category=item.get("category"),
            price=price_value,
        )
        db.add(db_obj)

    db.commit()
    return {"message": "Scraped data imported successfully"}


