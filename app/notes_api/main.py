"""
Notes API

A FastAPI application for managing notes using the file system. Each note is stored
as a separate text file, allowing for basic CRUD operations (Create, Read, Update, Delete).

Endpoints:
    POST /notes/{title} - Create a new note
    GET /notes/{title} - Read a note
    PUT /notes/{title} - Update a note
    DELETE /notes/{title} - Delete a note
"""

from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(
    title="Notes API",
    description="Simple note-taking API using file system storage",
    version="1.0.0"
)

# Create notes directory if it doesn't exist
NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

class Note(BaseModel):
    """
    Represents a note's content.

    Attributes:
        content (str): The text content of the note
    """
    content: str

def get_note_path(title: str) -> str:
    """
    Generate the full file path for a note.

    Args:
        title (str): The title of the note

    Returns:
        str: Full path to the note file
    """
    return os.path.join(NOTES_DIR, f"{title}.txt")

@app.post("/notes/{title}")
def create_note(title: str, note: Note):
    """
    Create a new note with the given title and content.

    Args:
        title (str): The title of the note (will be used as filename)
        note (Note): The note content

    Returns:
        dict: Success/error message

    Example:
        POST /notes/my-first-note
        Body: {"content": "This is my first note"}
    """
    try:
        file_path = get_note_path(title)
        with open(file_path, "w") as f:
            f.write(note.content)
        return {"message": f"Note '{title}' created successfully!"}
    except:
        return {"message": "Error creating note"}

@app.get("/notes/{title}")
def read_note(title: str):
    """
    Read a note's content.

    Args:
        title (str): The title of the note to read

    Returns:
        dict: Note title and content, or error message if not found

    Example:
        GET /notes/my-first-note
    """
    try:
        file_path = get_note_path(title)
        if not os.path.exists(file_path):
            return {"message": f"Note '{title}' not found"}
        with open(file_path, "r") as f:
            content = f.read()
        return {"title": title, "content": content}
    except:
        return {"message": "Error reading note"}

@app.put("/notes/{title}")
def update_note(title: str, note: Note):
    """
    Update an existing note's content.

    Args:
        title (str): The title of the note to update
        note (Note): The new note content

    Returns:
        dict: Success/error message

    Example:
        PUT /notes/my-first-note
        Body: {"content": "Updated content"}
    """
    try:
        file_path = get_note_path(title)
        if not os.path.exists(file_path):
            return {"message": f"Note '{title}' not found"}
        with open(file_path, "w") as f:
            f.write(note.content)
        return {"message": f"Note '{title}' updated successfully!"}
    except:
        return {"message": "Error updating note"}

@app.delete("/notes/{title}")
def delete_note(title: str):
    """
    Delete a note.

    Args:
        title (str): The title of the note to delete

    Returns:
        dict: Success/error message

    Example:
        DELETE /notes/my-first-note
    """
    try:
        file_path = get_note_path(title)
        if not os.path.exists(file_path):
            return {"message": f"Note '{title}' not found"}
        os.remove(file_path)
        return {"message": f"Note '{title}' deleted successfully!"}
    except:
        return {"message": "Error deleting note"}
