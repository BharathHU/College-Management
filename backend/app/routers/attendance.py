from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, Subject, User, Attendance, Teacher, TeacherSubject, Enrollment
from app.schemas.api import AttendanceCreate

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/student")
def student_attendance(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    rows = db.query(Attendance).filter(Attendance.student_id == student.id).all()
    return {"success": True, "data": [{"id": r.id, "subject": r.subject.name, "date": r.attendance_date.isoformat(), "status": r.status} for r in rows]}


@router.post("/mark")
def teacher_mark_attendance(payload: AttendanceCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    subject_id = payload.subject_id
    student_id = payload.student_id
    date_value = payload.date
    status = payload.status
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=403, detail="Teacher profile not found")
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if not db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher.id, TeacherSubject.subject_id == subject.id).first():
        raise HTTPException(status_code=403, detail="Teacher is not assigned this subject")
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(Enrollment).filter(Enrollment.student_id == student.id, Enrollment.subject_id == subject.id).first():
        raise HTTPException(status_code=400, detail="Student is not enrolled in this subject")
    existing = db.query(Attendance).filter(Attendance.student_id == student.id, Attendance.subject_id == subject.id, Attendance.attendance_date == date_value).first()
    if existing:
        raise HTTPException(status_code=409, detail="Attendance already exists for this date and subject")
    record = Attendance(student_id=student.id, subject_id=subject.id, attendance_date=date_value, status=status)
    db.add(record)
    db.commit()
    return {"success": True, "data": {"message": "Attendance recorded successfully"}}
