from sqlalchemy import case, func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.database import get_db
from app.dependencies.auth import require_role
from app.models.user import RoleEnum, Student, Teacher, User, Subject, Enrollment, Attendance, Mark, Assignment, AssignmentSubmission, Announcement, TeacherSubject, Timetable

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/student")
def get_student_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.STUDENT))):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        return {"success": True, "data": {"stats": {}, "attendance": [], "announcements": [], "upcoming_classes": []}}

    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student.id).all()
    subjects = [e.subject for e in enrollments]
    attendance_rows = db.query(Attendance).filter(Attendance.student_id == student.id).all()
    marks_rows = db.query(Mark).filter(Mark.student_id == student.id).all()
    subject_ids = [s.id for s in subjects]
    pending_assignments = db.query(func.count(Assignment.id)).outerjoin(
        AssignmentSubmission,
        (Assignment.id == AssignmentSubmission.assignment_id) & (AssignmentSubmission.student_id == student.id),
    ).filter(
        Assignment.subject_id.in_(subject_ids),
        (AssignmentSubmission.id.is_(None)) | (~AssignmentSubmission.status.in_(["submitted", "graded"])),
    ).scalar() if subject_ids else 0
    announcements = db.query(Announcement).filter((Announcement.subject_id.in_(subject_ids)) | Announcement.subject_id.is_(None)).order_by(Announcement.created_at.desc()).limit(5).all()
    upcoming_classes = db.query(Timetable).filter(Timetable.subject_id.in_(subject_ids)).order_by(Timetable.day_of_week, Timetable.start_time).all() if subject_ids else []
    grade_distribution = {}
    for mark in marks_rows:
        grade_distribution[mark.grade] = grade_distribution.get(mark.grade, 0) + 1

    total_attendance = 0
    total_classes = 0
    for row in attendance_rows:
        total_classes += 1
        if row.status.lower() == "present":
            total_attendance += 1
    overall_attendance = round((total_attendance / total_classes * 100), 2) if total_classes else 0

    total_marks = sum(m.total_marks for m in marks_rows)
    avg_marks = round(total_marks / len(marks_rows), 2) if marks_rows else 0

    return {
        "success": True,
        "data": {
            "welcome": f"Welcome, {student.first_name} {student.last_name}",
            "stats": {
                "overall_attendance": overall_attendance,
                "current_semester": student.semester,
                "number_of_subjects": len(subjects),
                "pending_assignments": pending_assignments,
                "average_marks": avg_marks,
            },
            "attendance": [{"subject": a.name, "percentage": round((sum(1 for x in attendance_rows if x.subject_id == a.id and x.status.lower() == "present") / max(sum(1 for x in attendance_rows if x.subject_id == a.id), 1)) * 100, 2) if any(x.subject_id == a.id for x in attendance_rows) else 0} for a in subjects],
            "announcements": [{"title": a.title, "message": a.message, "created_at": a.created_at.isoformat()} for a in announcements],
            "upcoming_classes": [{"subject": item.subject.name, "day": item.day_of_week, "start_time": item.start_time, "end_time": item.end_time, "room": item.room} for item in upcoming_classes],
            "grade_distribution": grade_distribution,
        },
    }


@router.get("/teacher")
def get_teacher_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_role(RoleEnum.TEACHER))):
    teacher_record = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher_record:
        return {"success": True, "data": {"stats": {}, "attendance": [], "announcements": [], "performance": []}}

    assigned_subjects = db.query(Subject).join(TeacherSubject, TeacherSubject.subject_id == Subject.id).filter(TeacherSubject.teacher_id == teacher_record.id).all()
    students = db.query(Student).join(Enrollment, Enrollment.student_id == Student.id).join(Subject, Subject.id == Enrollment.subject_id).filter(Subject.id.in_([s.id for s in assigned_subjects])).distinct().all()
    assignment_count = db.query(Assignment).filter(Assignment.teacher_id == teacher_record.id).count()
    attendance_rows = db.query(Attendance).join(Subject, Subject.id == Attendance.subject_id).join(TeacherSubject, TeacherSubject.subject_id == Subject.id).filter(TeacherSubject.teacher_id == teacher_record.id).all()
    present_count = sum(1 for row in attendance_rows if row.status.lower() == "present")
    attendance_overview = round((present_count / len(attendance_rows)) * 100, 2) if attendance_rows else 0
    announcements = db.query(Announcement).filter(Announcement.teacher_id == teacher_record.id).order_by(Announcement.created_at.desc()).limit(5).all()

    return {
        "success": True,
        "data": {
            "stats": {
                "assigned_subjects": len(assigned_subjects),
                "student_count": len(students),
                "attendance_overview": attendance_overview,
                "assignment_overview": assignment_count,
            },
            "attendance": [],
            "announcements": [{"title": a.title, "message": a.message, "created_at": a.created_at.isoformat()} for a in announcements],
            "performance": get_teacher_performance_data(db, teacher_record.id),
        },
    }


def get_teacher_performance_data(db: Session, teacher_id: int):
    results = []
    subjects = db.query(Subject).join(TeacherSubject, TeacherSubject.subject_id == Subject.id).filter(TeacherSubject.teacher_id == teacher_id).all()
    for subject in subjects:
        marks = db.query(Mark).filter(Mark.subject_id == subject.id).all()
        values = [mark.total_marks for mark in marks]
        results.append({"subject": subject.name, "average_marks": round(sum(values) / len(values), 2) if values else 0})
    return results
