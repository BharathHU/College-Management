from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import Announcement, RoleEnum, Subject, Teacher, TeacherSubject, User
from app.schemas.api import AnnouncementCreate

router = APIRouter(prefix="/announcements", tags=["announcements"])


@router.get("")
def list_announcements(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT, RoleEnum.TEACHER))):
    announcements = db.query(Announcement).order_by(Announcement.created_at.desc()).all()
    return {"success": True, "data": [{"id": a.id, "title": a.title, "description": a.message, "date": a.created_at.isoformat(), "teacher": a.teacher.first_name + " " + a.teacher.last_name, "subject": a.subject.name if a.subject else None} for a in announcements]}


@router.post("/create")
def create_announcement(payload: AnnouncementCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    subject_id = payload.subject_id
    if subject_id:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        if not db.query(Teacher).join(TeacherSubject, TeacherSubject.teacher_id == Teacher.id).filter(Teacher.id == teacher.id, TeacherSubject.subject_id == subject_id).first():
            raise HTTPException(status_code=403, detail="Teacher is not assigned this subject")
    announcement = Announcement(teacher_id=teacher.id, subject_id=subject_id, title=payload.title, message=payload.message)
    db.add(announcement)
    db.commit()
    return {"success": True, "data": {"id": announcement.id, "message": "Announcement created successfully"}}
