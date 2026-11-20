from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CourseDB, EnrollmentDB, StudentDB

router = APIRouter(prefix="/academic", tags=["Courses & Enrollments"])


class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


@router.post("/courses", status_code=201)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    existing = db.query(CourseDB).filter(
        CourseDB.title == data.title
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Course already exists")

    course = CourseDB(title=data.title)

    db.add(course)
    db.commit()
    db.refresh(course)

    return {"message": "Course created", "id": course.id, "title": course.title}


@router.post("/enrollments", status_code=201)
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == data.student_id
    ).first()

    course = db.query(CourseDB).filter(
        CourseDB.id == data.course_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(EnrollmentDB).filter(
        EnrollmentDB.student_id == data.student_id,
        EnrollmentDB.course_id == data.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Already enrolled")

    enrollment = EnrollmentDB(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return {"message": "Student enrolled successfully"}


@router.get("/enrollments")
def get_enrollments(db: Session = Depends(get_db)):

    records = (
        db.query(EnrollmentDB)
        .join(StudentDB)
        .join(CourseDB)
        .all()
    )

    return [
        {
            "enrollment_id": item.id,
            "student_name": item.student.name,
            "course": item.course.title
        }
        for item in records
    ]