import json
import csv
from fastapi import FastAPI, Query, requests, Request, UploadFile, HTTPException, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from helper import APIHelper
import csv

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
    return {"message": "Student updated successfully"} if result else HTTPException(status_code=404,
                                                                                    detail="Student not found")


# @app.post("/students/bulk_import")
# async def bulk_import_students(file: UploadFile):
#     if file.content_type != "text/csv":
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
#     content = await file.read()
#     csv_data = csv.DictReader(content.decode("utf-8").splitlines())
#     result = await api.bulk_import_students(csv_data)
#     return {"message": f"{result} students imported successfully"}


@app.get("/students")
async def search_students(limit: int = Query(...), offset: int = Query(...)):
    result = await api.get_all_students(limit=limit, offset=offset)
    return result


@app.post("/vaccination/{student_id}")
async def mark_vaccinated(student_id, vaccine, drive):
    result = await api.mark_vaccinated(student_id, vaccine, drive)
    return {"message": "Student marked as vaccinated"} if result else HTTPException(status_code=400,
                                                                                    detail="Vaccination update failed")


@app.post("/drive")
async def add_vaccination_drive(request: Request):
    data = await request.json()
    result = await api.add_vaccination_drive(data)
    return {"message": "Vaccination drive added successfully"} if result else HTTPException(status_code=400,
                                                                                            detail="Vaccination drive addition failed")


@app.get("/login")
async def login():
    result = await api.login()
    return result


@app.post("/bulk_import")
async def bulk_import_students(file: UploadFile):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    content = await file.read()
    decoded_content = content.decode("utf-8-sig")
    csv_data = csv.DictReader(decoded_content.splitlines())
    student_data = [row for row in csv_data]
    result = await api.bulk_import_students(student_data)
    return {"message": f"{result} students imported successfully"}


@app.get("/students/vaccinated")
async def get_vaccinated_students():
    result = await api.get_vaccinated_students()
    return result


@app.get('/drive')
async def get_vaccination_drives(limit: int = Query(...), offset: int = Query(...)):
    result = await api.get_vaccination_drives(limit=limit, offset=offset)
    return result


@app.put('/drive')
async def edit_vaccination_drive(request: Request):
    response = await request.json()
    drive_name = response.get("drive_name")
    drive_data = response.get("drive_data")
    result = await api.edit_vaccination_drive(drive_name, drive_data)
    return {"message": "Vaccination drive updated successfully"} if result else HTTPException(status_code=404,
                                                                                              detail="Vaccination drive not found")


@app.get('/drive/drive_names')
async def get_vaccination_drive_names():
    result = await api.get_vaccination_drive_names()
    return result


@app.get('/students/{student_id}')
async def get_student_by_id(student_id):
    result = await api.get_student_by_id(student_id)
    return result
