"""
Job Application Tracker API

A FastAPI application for tracking job applications. This API allows users to create,
list, and search job applications, with data persistence using JSON files.

Endpoints:
    POST /applications/ - Create a new job application
    GET /applications/ - List all applications
    GET /applications/search - Search applications by status
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from file_handler import save_to_json, load_from_json

app = FastAPI(
    title="Job Application Tracker",
    description="API for tracking job applications",
    version="1.0.0"
)

APPLICATIONS_FILE = "applications.json"

class JobApplication(BaseModel):
    """
    Represents a job application with basic information.

    Attributes:
        name (str): Name of the applicant
        company (str): Company being applied to
        position (str): Job position title
        status (str): Current application status (e.g., pending, accepted, rejected)
    """
    name: str
    company: str
    position: str
    status: str

@app.post("/applications/")
def create_application(application: JobApplication):
    """
    Create a new job application.

    Args:
        application (JobApplication): The job application details

    Returns:
        dict: Message confirming creation and application details

    Example:
        {
            "message": "Application saved!",
            "application": {
                "name": "John Doe",
                "company": "Tech Corp",
                "position": "Developer",
                "status": "pending"
            }
        }
    """
    applications = load_from_json(APPLICATIONS_FILE)
    applications.append({
        "name": application.name,
        "company": application.company,
        "position": application.position,
        "status": application.status
    })
    save_to_json(applications, APPLICATIONS_FILE)
    return {"message": "Application saved!", "application": application}

@app.get("/applications/")
def get_applications():
    """
    Retrieve all job applications.

    Returns:
        list: List of all job applications

    Example:
        [
            {
                "name": "John Doe",
                "company": "Tech Corp",
                "position": "Developer",
                "status": "pending"
            }
        ]
    """
    return load_from_json(APPLICATIONS_FILE)

@app.get("/applications/search")
def search_applications(status: str):
    """
    Search job applications by status.

    Args:
        status (str): Status to search for (e.g., pending, accepted, rejected)

    Returns:
        list: List of applications matching the status

    Example:
        GET /applications/search?status=pending
    """
    applications = load_from_json(APPLICATIONS_FILE)
    matching_applications = []
    for app in applications:
        if app["status"].lower() == status.lower():
            matching_applications.append(app)
    return matching_applications
