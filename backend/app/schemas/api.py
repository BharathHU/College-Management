from datetime import datetime

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AttendanceCreate(BaseModel):
    subject_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    date: datetime
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        normalized = value.lower()
        if normalized not in {"present", "absent"}:
            raise ValueError("Status must be present or absent")
        return normalized


class MarksUpsert(BaseModel):
    subject_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
    internal_marks: float = Field(ge=0, le=30)
    assignment_marks: float = Field(ge=0, le=20)
    exam_marks: float = Field(ge=0, le=50)


class AssignmentCreate(BaseModel):
    subject_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=1000)
    due_date: datetime


class AssignmentSubmissionCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class AssignmentSubmissionReview(BaseModel):
    status: Literal["submitted", "graded", "missing"]


class AnnouncementCreate(BaseModel):
    subject_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=2000)


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)