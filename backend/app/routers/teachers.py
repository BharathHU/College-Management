from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, User, Subject, Teacher, TeacherSubject, Enrollment, Attendance, Mark, Assignment, AssignmentSubmission, Announcement

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/me")
def get_teacher_profile(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return {"success": True, "data": {"id": teacher.id, "teacher_id": teacher.teacher_id, "first_name": teacher.first_name, "last_name": teacher.last_name, "email": current_user.email, "phone": teacher.phone, "department": teacher.department.name, "designation": teacher.designation}}


@router.get("/subjects")
def get_teacher_subjects(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER)), q: str | None = Query(None, max_length=100), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    query = db.query(Subject).join(TeacherSubject, TeacherSubject.subject_id == Subject.id).filter(TeacherSubject.teacher_id == teacher.id)
    if q:
        query = query.filter((Subject.name.ilike(f"%{q}%")) | (Subject.code.ilike(f"%{q}%")))
    total = query.count()
    linked = query.offset((page - 1) * limit).limit(limit).all()
    return {"success": True, "data": {"items": [{"id": s.id, "name": s.name, "code": s.code, "semester": s.semester, "department": s.department.name, "student_count": db.query(Enrollment).filter(Enrollment.subject_id == s.id).count()} for s in linked], "page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit if total else 0}}


@router.get("/students")
def get_teacher_students(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER)), subject_id: int | None = Query(None, gt=0), q: str | None = Query(None, max_length=100), limit: int = Query(20, ge=1, le=100), page: int = Query(1, ge=1)):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    query = db.query(
        Student,
        func.count(Attendance.id).label("attendance_total"),
        func.sum(case((Attendance.status == "present", 1), else_=0)).label("attendance_present"),
        func.max(Mark.total_marks).label("performance"),
    ).join(User, User.id == Student.user_id).join(Enrollment, Enrollment.student_id == Student.id).join(
        TeacherSubject, TeacherSubject.subject_id == Enrollment.subject_id
    ).outerjoin(
        Attendance, (Attendance.student_id == Student.id) & (Attendance.subject_id == Enrollment.subject_id)
    ).outerjoin(
        Mark, (Mark.student_id == Student.id) & (Mark.subject_id == Enrollment.subject_id)
    ).filter(TeacherSubject.teacher_id == teacher.id)
    if subject_id:
        query = query.filter(Enrollment.subject_id == subject_id)
    if q:
        query = query.filter((Student.first_name.ilike(f"%{q}%")) | (Student.last_name.ilike(f"%{q}%")) | (Student.student_id.ilike(f"%{q}%")))
    query = query.group_by(Student.id, Student.user_id, Student.student_id, Student.first_name, Student.last_name, User.email)
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    roster = []
    for student, attendance_total, attendance_present, performance in items:
        attendance = round((attendance_present / attendance_total) * 100, 2) if attendance_total else None
        roster.append({"id": student.id, "student_id": student.student_id, "name": f"{student.first_name} {student.last_name}", "email": student.user.email, "attendance": attendance, "performance": performance})
    return {"success": True, "data": {"items": roster, "page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit if total else 0}}


@router.get("/performance")
def get_teacher_performance(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    results = []
    for subject in db.query(Subject).join(TeacherSubject, TeacherSubject.subject_id == Subject.id).filter(TeacherSubject.teacher_id == teacher.id).all():
        marks = db.query(Mark).filter(Mark.subject_id == subject.id).all()
        averages = [m.total_marks for m in marks]
        results.append({"subject": subject.name, "average_marks": round(sum(averages) / len(averages), 2) if averages else 0, "highest": max(averages) if averages else 0, "lowest": min(averages) if averages else 0})
    return {"success": True, "data": results}
