from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, Subject, Teacher, TeacherSubject, Timetable, User, Enrollment

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("")
def list_timetable(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT, RoleEnum.TEACHER))):
    if current_user.role == RoleEnum.STUDENT:
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        subject_ids = [enrollment.subject_id for enrollment in student.enrollments] if student else []
        rows = db.query(Timetable).filter(Timetable.subject_id.in_(subject_ids)).all()
    else:
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        rows = db.query(Timetable).filter(Timetable.teacher_id == teacher.id if teacher else False).all()
    return {"success": True, "data": [{"day": r.day_of_week, "start_time": r.start_time, "end_time": r.end_time, "subject": r.subject.name, "teacher": next((f"{t.first_name} {t.last_name}" for t in db.query(Teacher).filter(Teacher.id == r.teacher_id).all()), "N/A"), "room": r.room} for r in rows]}
