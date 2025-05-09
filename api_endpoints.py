import json
import csv
from fastapi import FastAPI, Query, requests, Request, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from helper import APIHelper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

api = APIHelper()


@app.get("/dashboard")
async def dashboard():
    result = await api.get_dashboard_data()
    return result


@app.post("/students")
async def add_student(student: dict):
    result = await api.add_student(student)
    return {"message": "Student added successfully", "student_id": result}


@app.put("/students/{student_id}")
async def edit_student(student_id, student):
    result = await api.edit_student(student_id, student)
    return {"message": "Student updated successfully"} if result else HTTPException(status_code=404, detail="Student not found")


# @app.post("/students/bulk_import")
# async def bulk_import_students(file: UploadFile):
#     if file.content_type != "text/csv":
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
#     content = await file.read()
#     csv_data = csv.DictReader(content.decode("utf-8").splitlines())
#     result = await api.bulk_import_students(csv_data)
#     return {"message": f"{result} students imported successfully"}


@app.get("/students")
async def search_students(name: str = None, class_name: str = None, student_id: str = None, vaccinated: bool = None):
    query = {k: v for k, v in {"name": name, "class": class_name, "student_id": student_id, "vaccinated": vaccinated}.items() if v is not None}
    result = await api.search_students(query)
    return result


@app.post("/vaccination/{student_id}")
async def mark_vaccinated(student_id, vaccine, drive):
    result = await api.mark_vaccinated(student_id, vaccine, drive)
    return {"message": "Student marked as vaccinated"} if result else HTTPException(status_code=400, detail="Vaccination update failed")


@app.post("/drive")
async def add_vaccination_drive(drive_data):
    result = await api.add_vaccination_drive(drive_data)
    return {"message": "Vaccination drive added successfully"} if result else HTTPException(status_code=400, detail="Vaccination drive addition failed")


@app.get("/login")
async def login():
    result = await api.login()
    return result


@app.post("/bulk_import")
async def bulk_import_students(student_data):
    result = await api.bulk_import_students(student_data)
    return {"message": f"{result} students imported successfully"}


