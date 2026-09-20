from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, Subject, Teacher, TeacherSubject, User, Mark, Enrollment
from app.schemas.api import MarksUpsert

router = APIRouter(prefix="/marks", tags=["marks"])


@router.get("/student")
def student_marks(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    rows = db.query(Mark).filter(Mark.student_id == student.id).all()
    return {"success": True, "data": [{"subject": r.subject.name, "internal_marks": r.internal_marks, "assignment_marks": r.assignment_marks, "exam_marks": r.exam_marks, "total": r.total_marks, "grade": r.grade} for r in rows]}


@router.post("/upsert")
def teacher_upsert_marks(payload: MarksUpsert, db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    subject_id = payload.subject_id
    student_id = payload.student_id
    internal = payload.internal_marks
    assignment = payload.assignment_marks
    exam = payload.exam_marks
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject or not teacher:
        raise HTTPException(status_code=404, detail="Subject or teacher not found")
    if not db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher.id, TeacherSubject.subject_id == subject.id).first():
        raise HTTPException(status_code=403, detail="Teacher is not assigned this subject")
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(Enrollment).filter(Enrollment.student_id == student.id, Enrollment.subject_id == subject.id).first():
        raise HTTPException(status_code=400, detail="Student is not enrolled in this subject")
    total = internal + assignment + exam
    grade = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 55 else "D" if total >= 40 else "F"
    record = db.query(Mark).filter(Mark.student_id == student.id, Mark.subject_id == subject.id).first()
    if record:
        record.internal_marks = internal
        record.assignment_marks = assignment
        record.exam_marks = exam
        record.total_marks = total
        record.grade = grade
    else:
        record = Mark(student_id=student.id, subject_id=subject.id, internal_marks=internal, assignment_marks=assignment, exam_marks=exam, total_marks=total, grade=grade)
        db.add(record)
    db.commit()
    return {"success": True, "data": {"message": "Marks saved successfully", "total": total, "grade": grade}}
