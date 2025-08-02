# FastAPI Microservices Collection

A collection of simple, beginner-friendly FastAPI microservices for learning purposes.

## Services Overview

1. **Job Application Tracker API**
    - Track job applications with their status
    - Store applications in JSON file
    - Features:
        - Create new job applications
        - List all applications
        - Search applications by status

2. **Notes API**
    - Simple note-taking system using file storage
    - Features:
        - Create/Read/Update/Delete notes
        - Store notes as text files
        - Basic error handling

3. **Contacts API**
    - In-memory contact management system
    - Features:
        - Store contact information
        - Search contacts by name
        - Update and delete contacts

4. **Shopping Cart API**
    - Shopping cart functionality
    - Features:
        - Manage products
        - Handle cart operations
        - Store data in JSON files

5. **Student API**
    - Student information management
    - Features:
        - Store student data
        - JSON file-based storage

## Setup and Installation

1. Create a virtual environment:
   ```bash
   python -m venv librarybox
   ```

2. Activate the virtual environment:
    - Windows:
      ```bash
      librarybox\Scripts\activate
      ```
    - Unix/MacOS:
      ```bash
      source librarybox/bin/activate
      ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## Running the Services

Each service can be run independently using uvicorn. Navigate to the service directory and run:

```bash
uvicorn main:app --reload
```

For example, to run the Job Tracker API:
```bash
cd app/job_tracker_api
uvicorn main:app --reload
```

## API Documentation

After starting any service, you can access its interactive documentation at:
```
http://localhost:8000/docs
```

### Job Tracker API Endpoints
- `POST /applications/` - Create new job application
- `GET /applications/` - List all applications
- `GET /applications/search?status=pending` - Search by status

### Notes API Endpoints
- `POST /notes/{title}` - Create a note
- `GET /notes/{title}` - Read a note
- `PUT /notes/{title}` - Update a note
- `DELETE /notes/{title}` - Delete a note

### Contacts API Endpoints
- `POST /contacts/` - Create new contact
- `GET /contacts/` - List all contacts
- `GET /contacts/?name=John` - Search by name
- `PUT /contacts/{name}` - Update contact
- `DELETE /contacts/{name}` - Delete contact

## Project Structure
```
app/
├── job_tracker_api/
│   ├── main.py
│   └── file_handler.py
├── notes_api/
│   └── main.py
├── contacts_api/
│   └── main.py
├── shopping_cart_api/
│   └── main.py
└── student_api/
    └── main.py
```

## Error Handling
Each API implements basic error handling for common scenarios:
- File not found
- Invalid input
- Resource already exists
- Resource not found

## Data Storage
- Job Tracker API: JSON file (applications.json)
- Notes API: Text files in notes/ directory
- Contacts API: In-memory dictionary
- Shopping Cart API: JSON files
- Student API: JSON file

## Contributing
Feel free to submit issues and enhancement requests!
