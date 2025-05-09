# Vaccination Management System

This is a FastAPI-based application for managing student vaccination records and vaccination drives. It provides APIs for adding, editing, and retrieving student data, as well as managing vaccination drives.

## Features

- Add, edit, and search student records.
- Mark students as vaccinated.
- Manage vaccination drives.
- Dashboard with student and vaccination statistics.
- Bulk import of student data via CSV.

## Requirements

- Python 3.8+
- MongoDB

## Installation

Clone the repository

Install dependencies:
pip install -r requirements.txt
Ensure MongoDB is running locally on localhost:27017.

## Configuration

Usage

Start the FastAPI server:
uvicorn api_endpoints:app --host localhost --port 5000 --reload

Access the API documentation at:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints
API Endpoints
- **Students**
  - `GET /students`: Search for students based on query parameters.
  - `POST /students`: Add a new student.
  - `PUT /students/{student_id}`: Edit an existing student.
  - `POST /bulk_import`: Bulk import students from a JSON payload.
  - `GET /students/vaccinated`: Get a list of vaccinated students.
- **Vaccination**
  - `POST /vaccination/{student_id}`: Mark a student as vaccinated.
  - `POST /drive`: Add a new vaccination drive.
- **Dashboard**
  - `GET /dashboard`: Get statistics on students and vaccination drives.
- **Login**
  - `GET /login`: Dummy login endpoint.
- **Drives**
  - `POST /drive`: Add a new vaccination drive.

## Dependencies
Dependencies
fastapi==0.97.0
pytz~=2025.2
pymongo