from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# Directory to store notes
NOTES_DIR = "notes"

# Create notes directory if it doesn't exist
os.makedirs(NOTES_DIR, exist_ok=True)

class Note(BaseModel):
    content: str

def get_note_path(title: str) -> str:
    return os.path.join(NOTES_DIR, f"{title}.txt")

@app.post("/notes/{title}")
def create_note(title: str, note: Note):
    try:
        file_path = get_note_path(title)
        with open(file_path, "w") as f:
            f.write(note.content)
        return {"message": f"Note '{title}' created successfully!"}
    except:
        return {"message": "Error creating note"}

@app.get("/notes/{title}")
def read_note(title: str):
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
    try:
        file_path = get_note_path(title)
        if not os.path.exists(file_path):
            return {"message": f"Note '{title}' not found"}
        os.remove(file_path)
        return {"message": f"Note '{title}' deleted successfully!"}
    except:
        return {"message": "Error deleting note"}
