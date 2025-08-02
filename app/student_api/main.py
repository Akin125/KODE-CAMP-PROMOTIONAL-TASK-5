"""
Student Management API

A FastAPI application for managing student records including their subject scores,
calculating averages and grades. Data is persisted using JSON storage.

Features:
    - Add new students with subject scores
    - Calculate average scores automatically
    - Assign grades based on averages
    - Store data persistently in JSON format
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="Student Management System",
    description="API for managing student records and grades",
    version="1.0.0"
)

DATA_FILE = "students.json"

class Student(BaseModel):
    """
    Represents a student record with scores and calculated metrics.

    Attributes:
        name (str): Student's full name
        subject_scores (dict): Dictionary of subject names and their scores
        average (float): Calculated average score across all subjects
        grade (str): Letter grade based on average score
    """
    name: str
    subject_scores: dict
    average: float = 0
    grade: str = ""

def calculate_grade(avg: float) -> str:
    """
    Calculate letter grade based on numerical average.

    Args:
        avg (float): The numerical average score

    Returns:
        str: Letter grade (A, B, C, D, or F)
    """
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

def load_students() -> list:
    """
    Load student records from JSON file.

    Returns:
        list: List of student records, empty list if file doesn't exist
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(data: list) -> None:
    """
    Save student records to JSON file.

    Args:
        data (list): List of student records to save
    """
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
    """
    Add a new student record.

    Args:
        student (Student): The student data to add

    Returns:
        dict: Confirmation message

    Raises:
        HTTPException: If there is an error during addition
    """
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
    """
    Retrieve a student record by name.

    Args:
        name (str): The name of the student to retrieve

    Returns:
        dict: The student record

    Raises:
        HTTPException: If the student is not found or on other errors
    """
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
    """
    List all student records.

    Returns:
        list: A list of all student records

    Raises:
        HTTPException: If there is an error during retrieval
    """
    try:
        return load_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
