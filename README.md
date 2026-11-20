# Student Management API

A backend REST API built using **Python, FastAPI, and MySQL** to manage student records, authentication, courses, and enrollments.

The project demonstrates core backend development concepts, including CRUD operations, database integration, JWT authentication, API validation, middleware, file uploads, and automated testing.

## 🚀 Features

- **Student Management:** Create, read, update, and delete student records.
- **Search & Filtering:** Search students and filter records by course.
- **Sorting & Pagination:** Organize student records efficiently.
- **Authentication & Authorization:** User registration, login, password hashing, and JWT-based authentication.
- **Course Management:** Create and manage courses.
- **Student Enrollments:** Enroll students in courses using database relationships.
- **File Upload:** Upload supported PDF, JPG, and PNG files.
- **Middleware:** Request processing time tracking.
- **CORS:** Configured cross-origin access for frontend integration.
- **Background Tasks:** Demonstration of background task execution.
- **Error Handling:** HTTP exceptions and custom exception handling.
- **API Testing:** Automated tests using Pytest.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| MySQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation |
| JWT | Authentication |
| Argon2 | Password hashing |
| Pytest | API testing |
| Uvicorn | ASGI server |
| Swagger UI | API documentation and testing |
| Git & GitHub | Version control |

## 📁 Project Structure

```text
student-management-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── auth_router.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── students.py
│       ├── enrollments.py
│       └── files.py
│
├── uploads/
├── test_api.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Devloper-Ronak/student-management-api.git
```

### 2. Navigate to the project directory

```bash
cd student-management-api
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the root directory:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_management

SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

Replace the placeholder values with your own local database credentials and a securely generated secret key.

### 7. Create the MySQL database

Open MySQL and execute:

```sql
CREATE DATABASE student_management;
```

Make sure your MySQL server is running.

### 8. Run the application

```bash
uvicorn app.main:app --reload
```

The backend server will start at:

`http://127.0.0.1:8000`

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI Schema | http://127.0.0.1:8000/openapi.json |

You can explore endpoints, send API requests, and test responses directly through Swagger UI.

## 🔗 Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/students/` | Get all students |
| GET | `/students/{student_id}` | Get student by ID |
| POST | `/students/` | Create a student |
| PUT | `/students/{student_id}` | Update student |
| PATCH | `/students/{student_id}` | Partially update student |
| DELETE | `/students/{student_id}` | Delete student |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login and obtain JWT |
| GET | `/auth/me` | Get authenticated user |
| POST | `/academic/courses` | Create a course |
| POST | `/academic/enrollments` | Enroll a student |
| GET | `/academic/enrollments` | Get enrollments |
| POST | `/files/upload` | Upload a file |

## 🧪 Running Tests

Run the automated API tests using:

```bash
pytest -v
```

## 🔐 Security Notes

- Passwords are hashed using Argon2.
- JWT tokens are used for authentication.
- Sensitive configuration is stored in environment variables.
- The `.env` file should never be committed to GitHub.
- File uploads should be further hardened before production use.

## 🎯 Learning Outcomes

Through this project, I gained practical experience with:

- Building RESTful APIs using FastAPI
