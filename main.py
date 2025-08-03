from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
#######
app = FastAPI()

# In-memory storage
students = []
student_id_counter = 1

# Pydantic models
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str

class Student(StudentCreate):
    id: int

# Create student
@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate):
    global student_id_counter
    new_student = Student(id=student_id_counter, **student.dict())
    students.append(new_student)
    student_id_counter += 1
    return new_student

# Get all students
@app.get("/students/", response_model=List[Student])
def get_all_students():
    return students

# Get student by ID
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# Update student
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_data: StudentCreate):
    for index, student in enumerate(students):
        if student.id == student_id:
            updated_student = Student(id=student_id, **updated_data.dict())
            students[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

# Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            del students[index]
            return {"detail": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
