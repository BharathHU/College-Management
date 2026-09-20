from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, User, Student, Teacher, TeacherSubject, Subject, Assignment, AssignmentSubmission, Enrollment
from app.schemas.api import AssignmentCreate, AssignmentSubmissionCreate, AssignmentSubmissionReview

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/student")
def student_assignments(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT)), q: str | None = Query(None, min_length=1, max_length=100), status: str | None = Query(None), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    subject_ids = [e.subject_id for e in student.enrollments]
    query = db.query(Assignment).join(Subject).filter(Assignment.subject_id.in_(subject_ids))
    if q:
        query = query.filter((Assignment.title.ilike(f"%{q}%")) | (Assignment.description.ilike(f"%{q}%")) | (Subject.name.ilike(f"%{q}%")))
    assignments = query.order_by(Assignment.due_date).all()
    results = []
    for assignment in assignments:
        submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == assignment.id, AssignmentSubmission.student_id == student.id).first()
        status_value = submission.status.title() if submission else "Pending"
        results.append({"id": assignment.id, "title": assignment.title, "subject": assignment.subject.name, "description": assignment.description, "assigned_date": assignment.created_at.isoformat(), "due_date": assignment.due_date.isoformat(), "status": status_value, "submission_date": submission.submitted_at.isoformat() if submission else None, "submission": submission.content if submission else None})
    if status:
        results = [item for item in results if item["status"].lower() == status.lower()]
    total = len(results)
    start = (page - 1) * limit
    return {"success": True, "data": {"items": results[start:start + limit], "page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit if total else 0}}


@router.post("/create")
def create_assignment(payload: AssignmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    subject_id = payload.subject_id
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if not db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher.id, TeacherSubject.subject_id == subject.id).first():
        raise HTTPException(status_code=403, detail="Teacher is not assigned to this subject")
    assignment = Assignment(
        teacher_id=teacher.id,
        subject_id=subject.id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return {"success": True, "data": {"id": assignment.id, "message": "Assignment created successfully"}}


@router.get("/teacher")
def teacher_assignments(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER)), q: str | None = Query(None, min_length=1, max_length=100), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    query = db.query(Assignment).join(Subject).filter(Assignment.teacher_id == teacher.id)
    if q:
        query = query.filter((Assignment.title.ilike(f"%{q}%")) | (Assignment.description.ilike(f"%{q}%")) | (Subject.name.ilike(f"%{q}%")))
    total = query.count()
    assignments = query.order_by(Assignment.due_date).offset((page - 1) * limit).limit(limit).all()
    return {"success": True, "data": {"items": [{"id": assignment.id, "title": assignment.title, "subject": assignment.subject.name, "description": assignment.description, "due_date": assignment.due_date.isoformat(), "submission_count": db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == assignment.id).count()} for assignment in assignments], "page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit if total else 0}}


@router.post("/{assignment_id}/submit")
def submit_assignment(assignment_id: int, payload: AssignmentSubmissionCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment or not student:
        raise HTTPException(status_code=404, detail="Assignment or student not found")
    if not any(enrollment.subject_id == assignment.subject_id for enrollment in student.enrollments):
        raise HTTPException(status_code=403, detail="Student is not enrolled in this subject")
    submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == assignment.id, AssignmentSubmission.student_id == student.id).first()
    if submission:
        raise HTTPException(status_code=409, detail="Assignment has already been submitted")
    submission = AssignmentSubmission(assignment_id=assignment.id, student_id=student.id, submitted_at=datetime.utcnow(), status="submitted", content=payload.content)
    db.add(submission)
    db.commit()
    return {"success": True, "data": {"id": submission.id, "status": submission.status.title()}}


@router.get("/{assignment_id}/submissions")
def assignment_submissions(assignment_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.teacher_id == teacher.id if teacher else False).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    rows = db.query(Student, AssignmentSubmission).join(
        Enrollment, Enrollment.student_id == Student.id
    ).outerjoin(
        AssignmentSubmission,
        and_(AssignmentSubmission.assignment_id == assignment.id, AssignmentSubmission.student_id == Student.id),
    ).filter(Enrollment.subject_id == assignment.subject_id).all()
    results = []
    for student, submission in rows:
        if submission:
            status = submission.status.title()
            is_late = submission.submitted_at > assignment.due_date
            results.append({"id": submission.id, "assignment_id": assignment.id, "student_id": student.student_id, "student_name": f"{student.first_name} {student.last_name}", "status": "Late" if is_late and status == "Submitted" else status, "submitted_at": submission.submitted_at.isoformat(), "is_late": is_late, "content": submission.content})
        else:
            results.append({"id": None, "assignment_id": assignment.id, "student_id": student.student_id, "student_name": f"{student.first_name} {student.last_name}", "status": "Pending", "submitted_at": None, "is_late": False, "content": None})
    return {"success": True, "data": results}


@router.patch("/{assignment_id}/submissions/{submission_id}")
def update_submission_status(assignment_id: int, submission_id: int, payload: AssignmentSubmissionReview, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.teacher_id == teacher.id if teacher else False).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id, AssignmentSubmission.assignment_id == assignment.id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission.status = payload.status
    db.commit()
    return {"success": True, "data": {"id": submission.id, "status": submission.status}}
