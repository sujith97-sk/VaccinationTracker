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

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure MongoDB is running locally on `localhost:27017`.

## Configuration

No additional configuration is required.

## Usage

Start the FastAPI server:
```bash
uvicorn api_endpoints:app --host localhost --port 8000 --reload
```

Access the API documentation at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Dashboard

- **GET** `/dashboard`
  - **Description**: Fetch dashboard data including student count, vaccinated count, vaccination percentage, and upcoming drives.
  - **Response**:
    ```json
    {
      "student_count": 100,
      "vaccinated_count": 50,
      "vaccinated_percentage": 50.0,
      "upcoming_drives": [...]
    }
    ```

---

### Student Management

- **POST** `/students`
  - **Description**: Add a new student.
  - **Request Body**:
    ```json
    {
      "name": "John Doe",
      "roll_number": 123,
      "class": 10,
      "vaccinated": false
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Student added successfully",
      "student_id": "123"
    }
    ```

- **PUT** `/students/{student_id}`
  - **Description**: Edit student details.
  - **Request Body**:
    ```json
    {
      "name": "Jane Doe",
      "class": 11
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Student updated successfully"
    }
    ```

- **GET** `/students`
  - **Description**: Fetch all students with pagination.
  - **Query Parameters**:
    - `limit` (int): Number of students to fetch.
    - `offset` (int): Starting point for fetching students.
  - **Response**:
    ```json
    [
      {
        "name": "John Doe",
        "roll_number": 123,
        "class": 10,
        "vaccinated": false
      },
      ...
    ]
    ```

- **GET** `/students/{student_id}`
  - **Description**: Fetch a student by ID.
  - **Response**:
    ```json
    {
      "name": "John Doe",
      "roll_number": 123,
      "class": 10,
      "vaccinated": false
    }
    ```

- **POST** `/bulk_import`
  - **Description**: Bulk import students via CSV upload.
  - **Request**: Upload a CSV file with student details.
  - **Response**:
    ```json
    {
      "message": "50 students imported successfully"
    }
    ```

- **GET** `/students/vaccinated`
  - **Description**: Fetch vaccinated or unvaccinated students.
  - **Query Parameters**:
    - `vaccinated` (bool): `true` for vaccinated, `false` for unvaccinated.
  - **Response**:
    ```json
    [
      {
        "name": "John Doe",
        "roll_number": 123,
        "class": 10,
        "vaccinated": true
      },
      ...
    ]
    ```

- **GET** `/students/class`
  - **Description**: Fetch students by class.
  - **Query Parameters**:
    - `class_number` (int): Class number to filter students.
  - **Response**:
    ```json
    [
      {
        "name": "John Doe",
        "roll_number": 123,
        "class": 10,
        "vaccinated": false
      },
      ...
    ]
    ```

- **GET** `/students/vaccine`
  - **Description**: Fetch students by vaccine.
  - **Query Parameters**:
    - `vaccine` (str): Vaccine name to filter students.
  - **Response**:
    ```json
    [
      {
        "name": "John Doe",
        "roll_number": 123,
        "class": 10,
        "vaccinated": true,
        "vaccines": [
          {
            "vaccine": "COVID-19",
            "drive": "Drive 1",
            "date": "2023-12-01T10:00:00+05:30"
          }
        ]
      },
      ...
    ]
    ```

---

### Vaccination Management

- **POST** `/vaccination/mark_vaccinated`
  - **Description**: Mark a student as vaccinated in a specific drive.
  - **Request Body**:
    ```json
    {
      "student_id": 123,
      "drive": "Drive 1"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Student marked as vaccinated"
    }
    ```

- **GET** `/vaccination/vaccines`
  - **Description**: Fetch available vaccine names.
  - **Response**:
    ```json
    [
      "COVID-19",
      "Hepatitis B",
      ...
    ]
    ```

---

### Vaccination Drives

- **POST** `/drive`
  - **Description**: Add a new vaccination drive.
  - **Request Body**:
    ```json
    {
      "name": "Drive 1",
      "vaccine": "COVID-19",
      "scheduled_date": "2023-12-01T10:00:00+05:30"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Vaccination drive added successfully"
    }
    ```

- **GET** `/drive`
  - **Description**: Fetch all vaccination drives with pagination.
  - **Query Parameters**:
    - `limit` (int): Number of drives to fetch.
    - `offset` (int): Starting point for fetching drives.
  - **Response**:
    ```json
    [
      {
        "name": "Drive 1",
        "vaccine": "COVID-19",
        "scheduled_date": "2023-12-01T10:00:00+05:30"
      },
      ...
    ]
    ```

- **PUT** `/drive`
  - **Description**: Edit a vaccination drive.
  - **Request Body**:
    ```json
    {
      "drive_name": "Drive 1",
      "drive_data": {
        "vaccine": "COVID-19 Updated",
        "scheduled_date": "2023-12-05T10:00:00+05:30"
      }
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Vaccination drive updated successfully"
    }
    ```

- **GET** `/drive/drive_names`
  - **Description**: Fetch names of all vaccination drives.
  - **Response**:
    ```json
    [
      {
        "name": "Drive 1"
      },
      ...
    ]
    ```

---

## License

This project is licensed under the MIT License.
