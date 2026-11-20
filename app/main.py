
from fastapi import FastAPI, Request
from app.routers import enrollments
from app.database import engine, Base
from app import models
from app.routers import students
from app import auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers import files
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import time

app = FastAPI(
    title="Student Management API",
    description="Backend project using FastAPI and MySQL",
    version="1.0.0"
)
class CustomAppException(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(CustomAppException)
async def custom_exception_handler(
    request: Request,
    exc: CustomAppException
):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message}
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def send_notification(email: str):
    print(f"Notification sent to {email}")


@app.post("/send-notification")
def send_notification_api(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification, email)

    return {"message": "Notification scheduled"}
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    return response

@app.get("/divide")
def divide_numbers(a: float, b: float):

    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot divide by zero"
        )

    return {
        "result": a / b
    }
# Create missing database tables
Base.metadata.create_all(bind=engine)

@app.get("/sync")
def sync_route():
    return {"message": "Synchronous request"}


@app.get("/async")
async def async_route():
    return {"message": "Asynchronous request"}
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}
@app.get("/custom-error")
def custom_error():
    raise CustomAppException("Something went wrong")

app.include_router(students.router)
app.include_router(auth_router.router)
app.include_router(enrollments.router)
app.include_router(files.router)
