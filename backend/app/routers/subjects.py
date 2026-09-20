from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Subject, TeacherSubject, Teacher, User

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("")
def list_subjects(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT, RoleEnum.TEACHER)), q: str | None = Query(None), department: str | None = Query(None), semester: int | None = Query(None), page: int = 1, limit: int = 20):
    query = db.query(Subject)
    if q:
        query = query.filter((Subject.name.ilike(f"%{q}%")) | (Subject.code.ilike(f"%{q}%")))
    if department:
        query = query.filter(Subject.department_id == int(department))
    if semester:
        query = query.filter(Subject.semester == semester)
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    return {
        "success": True,
        "data": {
            "items": [{"id": s.id, "name": s.name, "code": s.code, "credits": s.credits, "semester": s.semester, "department": s.department.name, "teacher": next((f"{t.first_name} {t.last_name}" for t in db.query(Teacher).join(TeacherSubject, TeacherSubject.teacher_id == Teacher.id).filter(TeacherSubject.subject_id == s.id).all()), "N/A")} for s in items],
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit if total else 0,
        },
    }


@router.get("/{subject_id}")
def get_subject(subject_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT, RoleEnum.TEACHER))):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"success": True, "data": {"id": subject.id, "name": subject.name, "code": subject.code, "credits": subject.credits, "semester": subject.semester, "department": subject.department.name}}
