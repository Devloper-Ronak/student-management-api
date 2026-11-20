
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy.orm import Session
from typing import Literal
from app.database import get_db
from app.models import StudentDB

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# Pydantic request model
class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    course: str = Field(min_length=2, max_length=30)
    age: int = Field(gt=17, lt=100)


# Partial update model
class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    course: str | None = Field(default=None, min_length=2, max_length=30)
    age: int | None = Field(default=None, gt=17, lt=100)


# Response model
class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str
    age: int

    model_config = ConfigDict(from_attributes=True)



# SEARCH + FILTER + SORT + PAGINATION
@router.get("/")
def get_students(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = None,
    course: str | None = None,
    sort_by: Literal["id", "name", "age"] = "id",
    order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db)
):
    query = db.query(StudentDB)

    # Search by name or email
    if search:
        query = query.filter(
            (StudentDB.name.ilike(f"%{search}%")) |
            (StudentDB.email.ilike(f"%{search}%"))
        )

    # Filter by course
    if course:
        query = query.filter(
            StudentDB.course.ilike(course)
        )

    # Count matching records before pagination
    total = query.count()

    # Sorting
    sort_column = getattr(StudentDB, sort_by)

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Pagination
    offset = (page - 1) * limit

    students = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "students": students
    }


# GET student by ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# CREATE student
@router.post("/", status_code=201, response_model=StudentResponse)
def create_student(student: Student, db: Session = Depends(get_db)):

    existing = db.query(StudentDB).filter(
        StudentDB.email == student.email
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    new_student = StudentDB(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# PUT - Complete update
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: Student,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_email = db.query(StudentDB).filter(
        StudentDB.email == student_data.email,
        StudentDB.id != student_id
    ).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    for key, value in student_data.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# PATCH - Partial update
@router.patch("/{student_id}", response_model=StudentResponse)
def partial_update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.query(StudentDB).filter(
            StudentDB.email == update_data["email"],
            StudentDB.id != student_id
        ).first()

        if existing_email:
            raise HTTPException(status_code=409, detail="Email already exists")

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# DELETE student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
