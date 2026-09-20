from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.models.user import *  # noqa: F401,F403
from app.routers import auth, dashboard, students, subjects, teachers, attendance, marks, assignments, announcements, timetable

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.backend_cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(teachers.router, prefix="/api")
app.include_router(subjects.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(marks.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")
app.include_router(announcements.router, prefix="/api")
app.include_router(timetable.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
