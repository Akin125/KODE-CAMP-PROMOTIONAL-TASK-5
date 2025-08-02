"""
Contacts API

A FastAPI application for managing contacts using in-memory storage.
Provides basic CRUD operations for contact management with search functionality.

Endpoints:
    POST /contacts/ - Create a new contact
    GET /contacts/ - List all contacts or search by name
    PUT /contacts/{name} - Update a contact
    DELETE /contacts/{name} - Delete a contact
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Contacts API",
    description="Simple contact management API with in-memory storage",
    version="1.0.0"
)

# In-memory storage for contacts
contacts = {}

class Contact(BaseModel):
    """
    Represents a contact's information.

    Attributes:
        name (str): Name of the contact
        phone (str): Phone number
        email (str): Email address
    """
    name: str
    phone: str
    email: str

@app.post("/contacts/")
def create_contact(contact: Contact):
    """
    Create a new contact.

    Args:
        contact (Contact): The contact information

    Returns:
        dict: Success/error message and contact details

    Example:
        POST /contacts/
        Body: {
            "name": "John Doe",
            "phone": "1234567890",
            "email": "john@example.com"
        }
    """
    # Check if contact already exists
    if contact.name in contacts:
        return {"message": "Contact already exists"}

    # Add new contact to our dictionary
    contacts[contact.name] = contact.dict()

    return {"message": "Contact created!", "contact": contact}

@app.get("/contacts/")
def get_contacts(name: str = None):
    """
    Get all contacts or search for a specific contact by name.

    Args:
        name (str, optional): Name to search for

    Returns:
        dict/list: Single contact if name provided, or all contacts

    Example:
        GET /contacts/ - Get all contacts
        GET /contacts/?name=John - Search for John
    """
    # If name is provided, return just that contact
    if name:
        if name in contacts:
            return contacts[name]
        return {"message": "Contact not found"}

    # If no name provided, return all contacts
    return contacts

@app.put("/contacts/{name}")
def update_contact(name: str, contact: Contact):
    """
    Update an existing contact's information.

    Args:
        name (str): Name of the contact to update
        contact (Contact): New contact information

    Returns:
        dict: Success/error message and updated contact

    Example:
        PUT /contacts/John
        Body: {
            "name": "John Doe",
            "phone": "0987654321",
            "email": "johndoe@example.com"
        }
    """
    # Check if contact exists
    if name not in contacts:
        return {"message": "Contact not found"}

    # Update contact information
    contacts[name] = contact.dict()

    return {"message": "Contact updated!", "contact": contacts[name]}

@app.delete("/contacts/{name}")
def delete_contact(name: str):
    """
    Delete a contact.

    Args:
        name (str): Name of the contact to delete

    Returns:
        dict: Success/error message and deleted contact info

    Example:
        DELETE /contacts/John
    """
    # Check if contact exists
    if name not in contacts:
        return {"message": "Contact not found"}

    # Remove contact from dictionary
    deleted_contact = contacts.pop(name)
    return {"message": "Contact deleted!", "contact": deleted_contact}
