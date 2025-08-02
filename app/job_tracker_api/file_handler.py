"""
File Handler Module for Job Application Tracker

This module provides functions for reading and writing job application data to JSON files.
It handles basic file operations with error handling for better reliability.

Functions:
    save_to_json(data, filename): Saves data to a JSON file
    load_from_json(filename): Loads data from a JSON file
"""

import json

def save_to_json(data, filename):
    """
    Save data to a JSON file.

    Args:
        data: The data to save (typically a list of dictionaries)
        filename (str): Name of the file to save to

    Raises:
        Exception: If there's an error writing to the file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def load_from_json(filename):
    """
    Load data from a JSON file.

    Args:
        filename (str): Name of the file to load from

    Returns:
        list: List of data from the JSON file, or empty list if file doesn't exist

    Raises:
        Exception: If there's an error reading the file
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading from file: {str(e)}")
        return []
