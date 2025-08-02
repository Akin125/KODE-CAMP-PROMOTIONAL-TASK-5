from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "students.json"

class Student(BaseModel):
    name: str
    subject_scores: dict
    average: float = 0
    grade: str = ""

def calculate_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 45:
        return "D"
    else:
        return "F"

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.post("/students/",
    response_model=dict,
    summary="Add a new student",
    description="Add a new student with their name and subject scores",
    response_description="Confirmation message upon successful addition",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "name": "John Doe",
                        "subject_scores": {
                            "Math": 80,
                            "English": 70,
                            "Biology": 90
                        }
                    }
                }
            }
        }
    }
)
def add_student(student: Student):
    try:
        scores = list(student.subject_scores.values())
        student.average = sum(scores) / len(scores)
        student.grade = calculate_grade(student.average)

        data = load_students()
        data.append(student.model_dump())
        save_students(data)
        return {"message": "Student added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/{name}")
def get_student(name: str):
    try:
        data = load_students()
        for student in data:
            if student['name'].lower() == name.lower():
                return student
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/")
def list_students():
    try:
        return load_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
