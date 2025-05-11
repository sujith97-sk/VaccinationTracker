import os
import json
from datetime import datetime, timedelta
import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


# FastAPI App
app = FastAPI()

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


async def login(user_data):
    return True


class APIHelper:
    def __init__(self):
        self.client = None
        self.database = None
        self.collection = None

    def create_connection(self, collection='Students'):
        try:
            self.client = MongoClient("localhost", 27017)
            mongo_db = self.client["FSA_Assignment"]
        except Exception as err:
            raise Exception("Unable to load Mongo DB: {0}".format(err))
        collection = mongo_db[collection]
        return collection

    def close_connection(self):
        if self.client:
            self.client.close()

    @staticmethod
    def get_documents_list(collection, query):
        documents = list(collection.find(query))
        return documents

    @staticmethod
    async def login():
        return True

    async def get_student_count(self):
        collection = self.create_connection()
        count = collection.count_documents({})
        self.close_connection()
        return count

    async def get_vaccinated_count(self):
        collection = self.create_connection()
        count = collection.count_documents({"vaccinated": True})
        self.close_connection()
        return count

    async def get_upcoming_drives(self):
        collection = self.create_connection("Drives")
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(ist)
        fifteen_days_later = current_time + timedelta(days=15)
        iso_current = current_time.strftime('%Y-%m-%dT%H:%M:%S+05:30')
        iso_fifteen = fifteen_days_later.strftime('%Y-%m-%dT%H:%M:%S+05:30')
        print(iso_current, iso_fifteen)
        query = {
            "scheduled_date": {"$gte": iso_current, "$lte": iso_fifteen}
        }
        documents = collection.find(query, {"_id": 0})
        return list(documents)

    async def get_dashboard_data(self):
        student_count = await self.get_student_count()
        vaccinated_count = await self.get_vaccinated_count()
        drives = await self.get_upcoming_drives()
        vaccinated_percentage = round(vaccinated_count/student_count * 100, 2) if vaccinated_count else 0
        return {"student_count": student_count, "vaccinated_count": vaccinated_count,
                "vaccinated_percentage": vaccinated_percentage, "upcoming_drives": drives}

    async def add_student(self, student):
        collection = self.create_connection()
        result = collection.insert_one(student)
        self.close_connection()
        return str(result.inserted_id)

    async def edit_student(self, student_id, student):
        collection = self.create_connection()
        result = collection.update_one({"roll_number": student_id}, {"$set": student})
        self.close_connection()
        return result.modified_count > 0

    async def bulk_import_students(self, csv_data):
        collection = self.create_connection()
        students = list(csv_data)
        for student in students:
            student["vaccinated"] = False
            student["vaccines"] = []
        result = collection.insert_many(students)
        self.close_connection()
        return len(result.inserted_ids) + 1

    async def search_students(self, query):
        collection = self.create_connection()
        students = self.get_documents_list(collection, query)
        self.close_connection()
        return students

    async def get_all_students(self, offset=0, limit=10):
        collection = self.create_connection()
        students = list(collection.find({}, {"_id": 0}).skip(offset).limit(limit))
        self.close_connection()
        return students

    async def get_vaccinated_students(self):
        collection = self.create_connection()
        students = self.get_documents_list(collection, {"vaccinated": True})
        self.close_connection()
        return students

    async def mark_vaccinated(self, student_id, drive):
        collection = self.create_connection()
        drive_collection = self.create_connection("Drives")
        vaccine = drive_collection.find_one({"name": drive}).get("vaccine")
        date = drive_collection.find_one({"name": drive}).get("scheduled_date")
        student = collection.find_one({"roll_number": student_id})
        if not student:
            self.close_connection()
            return False
        vaccination_record = student.get("vaccines", [])
        if student.get('vaccinated', False):
            for record in vaccination_record:
                if record["vaccine"] == vaccine and record["drive"] == drive:
                    self.close_connection()
                    return False
        vaccination_record.append({"vaccine": vaccine, "drive": drive, "date": date})
        result = collection.update_one({"roll_number": student_id}, {"$set": {"vaccines": vaccination_record,
                                                                              "vaccinated": True}})
        self.close_connection()
        return result.modified_count > 0

    async def add_vaccination_drive(self, drive_data):
        collection = self.create_connection("Drives")
        result = collection.insert_one(drive_data)
        self.close_connection()
        return result.inserted_id

    async def get_vaccination_drives(self, limit, offset):
        collection = self.create_connection("Drives")
        drives = list(collection.find({}, {"_id": 0}).skip(offset).limit(limit))
        self.close_connection()
        return drives

    async def edit_vaccination_drive(self, drive_name, drive_data):
        collection = self.create_connection("Drives")
        result = collection.update_one({"name": drive_name}, {"$set": drive_data})
        self.close_connection()
        return result.modified_count > 0

    async def get_vaccination_drive_names(self):
        collection = self.create_connection("Drives")
        drives = list(collection.find({}, {"_id": 0, "name": 1}))
        self.close_connection()
        return drives

    async def get_student_by_id(self, student_id):
        collection = self.create_connection()
        student = collection.find_one({"roll_number": student_id}, {"_id": 0})
        self.close_connection()
        return student
