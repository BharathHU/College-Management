from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, User, Enrollment, Subject, Attendance, Mark, Assignment, AssignmentSubmission, Announcement, Teacher, TeacherSubject, Timetable

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/me")
def get_student_profile(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return {"success": True, "data": {"id": student.id, "student_id": student.student_id, "first_name": student.first_name, "last_name": student.last_name, "email": current_user.email, "phone": student.phone, "department": student.department.name, "semester": student.semester, "profile_info": student.profile_info}}


@router.get("/subjects")
def get_student_subjects(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT)), q: str | None = Query(None), department: str | None = Query(None), semester: int | None = Query(None), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    query = db.query(Subject).join(Enrollment, Enrollment.subject_id == Subject.id).filter(Enrollment.student_id == student.id)
    if q:
        query = query.filter((Subject.name.ilike(f"%{q}%")) | (Subject.code.ilike(f"%{q}%")))
    if department:
        query = query.filter(Subject.department_id == int(department))
    if semester:
        query = query.filter(Subject.semester == semester)
    total = query.count()
    subjects = query.offset((page - 1) * limit).limit(limit).all()
    return {"success": True, "data": {"items": [{"id": s.id, "name": s.name, "code": s.code, "credits": s.credits, "semester": s.semester, "department": s.department.name, "teacher": next((f"{teacher.first_name} {teacher.last_name}" for teacher in db.query(Teacher).join(TeacherSubject, TeacherSubject.teacher_id == Teacher.id).filter(TeacherSubject.subject_id == s.id).all()), "N/A")} for s in subjects], "page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit if total else 0}}


@router.get("/attendance")
def get_student_attendance(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT)), q: str | None = Query(None, max_length=100)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    rows = db.query(Attendance).filter(Attendance.student_id == student.id).all()
    data = []
    subject_query = db.query(Subject).join(Enrollment, Enrollment.subject_id == Subject.id).filter(Enrollment.student_id == student.id)
    if q:
        subject_query = subject_query.filter((Subject.name.ilike(f"%{q}%")) | (Subject.code.ilike(f"%{q}%")))
    for subject in subject_query.all():
        subject_rows = [r for r in rows if r.subject_id == subject.id]
        present = sum(1 for r in subject_rows if r.status.lower() == "present")
        absent = sum(1 for r in subject_rows if r.status.lower() == "absent")
        total = len(subject_rows)
        percentage = round((present / total) * 100, 2) if total else 0
        data.append({"subject": subject.name, "total_classes": total, "present": present, "absent": absent, "percentage": percentage})
    return {"success": True, "data": data}


@router.get("/marks")
def get_student_marks(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT)), q: str | None = Query(None, max_length=100)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    marks_query = db.query(Mark).filter(Mark.student_id == student.id)
    if q:
        marks_query = marks_query.join(Subject).filter((Subject.name.ilike(f"%{q}%")) | (Subject.code.ilike(f"%{q}%")))
    marks = marks_query.all()
    return {"success": True, "data": [{"subject": m.subject.name, "internal_marks": m.internal_marks, "assignment_marks": m.assignment_marks, "exam_marks": m.exam_marks, "total": m.total_marks, "grade": m.grade} for m in marks]}


@router.get("/assignments")
def get_student_assignments(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT)), status: str | None = None):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    subjects = [e.subject_id for e in db.query(Enrollment).filter(Enrollment.student_id == student.id).all()]
    assignments = db.query(Assignment).filter(Assignment.subject_id.in_(subjects)).all()
    results = []
    for assignment in assignments:
        submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == assignment.id, AssignmentSubmission.student_id == student.id).first()
        status_value = "Pending"
        if submission:
            status_value = submission.status.title()
        results.append({"id": assignment.id, "title": assignment.title, "subject": assignment.subject.name, "description": assignment.description, "assigned_date": assignment.created_at.isoformat(), "due_date": assignment.due_date.isoformat(), "status": status_value})
    if status:
        results = [r for r in results if r["status"].lower() == status.lower()]
    return {"success": True, "data": results}


@router.get("/timetable")
def get_student_timetable(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    subject_ids = [e.subject_id for e in db.query(Enrollment).filter(Enrollment.student_id == student.id).all()]
    entries = db.query(Timetable).filter(Timetable.subject_id.in_(subject_ids)).order_by(Timetable.day_of_week, Timetable.start_time).all()
    return {"success": True, "data": [{"id": entry.id, "day": entry.day_of_week, "start_time": entry.start_time, "end_time": entry.end_time, "subject": entry.subject.name, "teacher": f"{entry.teacher.first_name} {entry.teacher.last_name}" if entry.teacher else "N/A", "room": entry.room} for entry in entries]}


@router.get("/announcements")
def get_student_announcements(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    subject_ids = [e.subject_id for e in db.query(Enrollment).filter(Enrollment.student_id == student.id).all()]
    announcements = db.query(Announcement).filter((Announcement.subject_id.in_(subject_ids)) | (Announcement.subject_id.is_(None))).order_by(Announcement.created_at.desc()).all()
    return {"success": True, "data": [{"id": a.id, "title": a.title, "description": a.message, "date": a.created_at.isoformat(), "teacher": a.teacher.first_name + " " + a.teacher.last_name, "subject": a.subject.name if a.subject else None} for a in announcements]}


@router.get("/performance")
def get_student_performance(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    marks = db.query(Mark).filter(Mark.student_id == student.id).all()
    return {"success": True, "data": {"average": round(sum(m.total_marks for m in marks) / len(marks), 2) if marks else 0, "subjects": [{"name": m.subject.name, "total": m.total_marks, "grade": m.grade} for m in marks], "grade_distribution": []}}
