from datetime import datetime, timedelta

from app.database import SessionLocal
from app.core.security import hash_password
from app.models.user import (
    Announcement,
    Assignment,
    AssignmentSubmission,
    Attendance,
    Department,
    Enrollment,
    Mark,
    Student,
    Subject,
    Teacher,
    TeacherSubject,
    Timetable,
    User,
    RoleEnum,
)


def seed():
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # CHECK WHETHER DATABASE IS ALREADY SEEDED
        # ---------------------------------------------------------
        # if db.query(User).filter(User.email == "student@example.com").first():
        #     print("Database already contains seed data.")
        #     return

        # ---------------------------------------------------------
        # CLEAR EXISTING SEED DATA
        # ---------------------------------------------------------
        db.query(Announcement).delete()
        db.query(AssignmentSubmission).delete()
        db.query(Assignment).delete()
        db.query(Attendance).delete()
        db.query(Mark).delete()
        db.query(Timetable).delete()
        db.query(TeacherSubject).delete()
        db.query(Enrollment).delete()
        db.query(Student).delete()
        db.query(Teacher).delete()
        db.query(Subject).delete()
        db.query(Department).delete()
        db.query(User).delete()

        db.commit()

        # =========================================================
        # DEPARTMENTS
        # =========================================================

        departments = [
            Department(
                name="Computer Science",
                code="CSE",
                description="Computer science and engineering",
            ),
            Department(
                name="Information Technology",
                code="IT",
                description="Information technology",
            ),
            Department(
                name="Electronics",
                code="ECE",
                description="Electronics and communication",
            ),
        ]

        db.add_all(departments)
        db.commit()

        # =========================================================
        # TEACHER USER
        # =========================================================

        teacher_user = User(
            email="teacher@example.com",
            username="teacher",
            password_hash=hash_password("teacher123"),
            role=RoleEnum.TEACHER,
            is_active=True,
        )

        db.add(teacher_user)
        db.commit()

        # =========================================================
        # PROVISIONED STUDENT USERS
        # =========================================================
        #
        # The assessment allows:
        # "student registration/login or provisioned student login"
        #
        # These accounts are provisioned through seed/demo data.
        # There is no public student registration page.
        #
        # Demo password for all students:
        # student123
        #
        # =========================================================

        student_users = [
            User(
                email="student@example.com",
                username="student",
                password_hash=hash_password("student123"),
                role=RoleEnum.STUDENT,
                is_active=True,
            ),
            User(
                email="priya@example.com",
                username="priya",
                password_hash=hash_password("student123"),
                role=RoleEnum.STUDENT,
                is_active=True,
            ),
            User(
                email="arjun@example.com",
                username="arjun",
                password_hash=hash_password("student123"),
                role=RoleEnum.STUDENT,
                is_active=True,
            ),
            User(
                email="neha@example.com",
                username="neha",
                password_hash=hash_password("student123"),
                role=RoleEnum.STUDENT,
                is_active=True,
            ),
            User(
                email="vijay@example.com",
                username="vijay",
                password_hash=hash_password("student123"),
                role=RoleEnum.STUDENT,
                is_active=True,
            ),
        ]

        db.add_all(student_users)
        db.commit()

        # =========================================================
        # TEACHER PROFILE
        # =========================================================

        teacher = Teacher(
            user_id=teacher_user.id,
            teacher_id="TCH-101",
            first_name="Aisha",
            last_name="Patel",
            phone="9876543210",
            designation="Assistant Professor",
            department_id=departments[0].id,
        )

        db.add(teacher)
        db.commit()

        # =========================================================
        # STUDENT PROFILES
        # =========================================================

        students = [
            Student(
                user_id=student_users[0].id,
                student_id="STU-1001",
                first_name="Rahul",
                last_name="Sharma",
                phone="9123456789",
                semester=5,
                profile_info=(
                    "Academic focus: data structures and "
                    "software engineering"
                ),
                department_id=departments[0].id,
            ),
            Student(
                user_id=student_users[1].id,
                student_id="STU-1002",
                first_name="Priya",
                last_name="Patel",
                phone="9123456790",
                semester=5,
                profile_info=(
                    "Academic focus: database systems and "
                    "web development"
                ),
                department_id=departments[0].id,
            ),
            Student(
                user_id=student_users[2].id,
                student_id="STU-1003",
                first_name="Arjun",
                last_name="Kumar",
                phone="9123456791",
                semester=5,
                profile_info=(
                    "Academic focus: Python programming and "
                    "backend development"
                ),
                department_id=departments[0].id,
            ),
            Student(
                user_id=student_users[3].id,
                student_id="STU-1004",
                first_name="Neha",
                last_name="Reddy",
                phone="9123456792",
                semester=5,
                profile_info=(
                    "Academic focus: frontend and "
                    "full-stack development"
                ),
                department_id=departments[0].id,
            ),
            Student(
                user_id=student_users[4].id,
                student_id="STU-1005",
                first_name="Vijay",
                last_name="Kumar",
                phone="9123456793",
                semester=5,
                profile_info=(
                    "Academic focus: SQL and "
                    "software engineering"
                ),
                department_id=departments[0].id,
            ),
        ]

        db.add_all(students)
        db.commit()

        # =========================================================
        # SUBJECTS
        # =========================================================

        subjects = [
            Subject(
                name="Python Programming",
                code="CS101",
                credits=4,
                semester=5,
                department_id=departments[0].id,
                description="Core programming and automation",
            ),
            Subject(
                name="Database Management Systems",
                code="CS102",
                credits=4,
                semester=5,
                department_id=departments[0].id,
                description="Relational data modeling and SQL",
            ),
            Subject(
                name="Web Development",
                code="CS103",
                credits=3,
                semester=5,
                department_id=departments[0].id,
                description="Frontend and backend web development",
            ),
        ]

        db.add_all(subjects)
        db.commit()

        # =========================================================
        # TEACHER-SUBJECT ASSIGNMENTS
        # =========================================================

        for subject in subjects:
            db.add(
                TeacherSubject(
                    teacher_id=teacher.id,
                    subject_id=subject.id,
                )
            )

        db.commit()

        # =========================================================
        # STUDENT ENROLLMENTS
        # =========================================================

        for student in students:
            for subject in subjects:
                db.add(
                    Enrollment(
                        student_id=student.id,
                        subject_id=subject.id,
                    )
                )

        db.commit()

        # =========================================================
        # ATTENDANCE
        # =========================================================
        #
        # Different students receive different attendance patterns
        # so dashboards and teacher reports look realistic.
        #
        # Student 1 -> High attendance
        # Student 2 -> Good attendance
        # Student 3 -> Average attendance
        # Student 4 -> Lower attendance
        # Student 5 -> Very good attendance
        #
        # =========================================================

        attendance_patterns = [
            ["present", "present", "present", "present", "absent", "present"],
            ["present", "present", "absent", "present", "present", "present"],
            ["present", "absent", "present", "absent", "present", "present"],
            ["absent", "present", "absent", "present", "absent", "present"],
            ["present", "present", "present", "present", "present", "absent"],
        ]

        today = datetime.utcnow()

        for student_index, student in enumerate(students):
            pattern = attendance_patterns[student_index]

            for subject in subjects:
                for offset, status in enumerate(pattern, start=1):
                    attendance_date = today - timedelta(days=offset)

                    db.add(
                        Attendance(
                            student_id=student.id,
                            subject_id=subject.id,
                            attendance_date=attendance_date,
                            status=status,
                        )
                    )

        db.commit()

        # =========================================================
        # MARKS
        # =========================================================
        #
        # Different marks for different students.
        # This gives meaningful data for grade distribution
        # and academic performance charts.
        #
        # =========================================================

        marks_data = [
            {
                "internal": 25,
                "assignment": 18,
                "exam": 45,
                "total": 88,
                "grade": "A",
            },
            {
                "internal": 23,
                "assignment": 17,
                "exam": 42,
                "total": 82,
                "grade": "A",
            },
            {
                "internal": 20,
                "assignment": 16,
                "exam": 38,
                "total": 74,
                "grade": "B",
            },
            {
                "internal": 18,
                "assignment": 14,
                "exam": 32,
                "total": 64,
                "grade": "C",
            },
            {
                "internal": 24,
                "assignment": 18,
                "exam": 44,
                "total": 86,
                "grade": "A",
            },
        ]

        for student_index, student in enumerate(students):
            marks = marks_data[student_index]

            for subject in subjects:
                db.add(
                    Mark(
                        student_id=student.id,
                        subject_id=subject.id,
                        internal_marks=marks["internal"],
                        assignment_marks=marks["assignment"],
                        exam_marks=marks["exam"],
                        total_marks=marks["total"],
                        grade=marks["grade"],
                    )
                )

        db.commit()

        # =========================================================
        # ASSIGNMENTS
        # =========================================================

        python_assignment = Assignment(
            teacher_id=teacher.id,
            subject_id=subjects[0].id,
            title="Python Mini Project",
            description=(
                "Build a CLI-based learning dashboard "
                "using Python."
            ),
            due_date=today + timedelta(days=10),
        )

        db.add(python_assignment)
        db.commit()

        database_assignment = Assignment(
            teacher_id=teacher.id,
            subject_id=subjects[1].id,
            title="SQL Database Design",
            description=(
                "Design a relational database and write "
                "queries for student management."
            ),
            due_date=today + timedelta(days=14),
        )

        db.add(database_assignment)
        db.commit()

        web_assignment = Assignment(
            teacher_id=teacher.id,
            subject_id=subjects[2].id,
            title="Full Stack Web Application",
            description=(
                "Build a responsive full-stack web application "
                "with REST APIs."
            ),
            due_date=today + timedelta(days=18),
        )

        db.add(web_assignment)
        db.commit()

        # =========================================================
        # ASSIGNMENT SUBMISSIONS
        # =========================================================

        submissions = [
            AssignmentSubmission(
                assignment_id=python_assignment.id,
                student_id=students[0].id,
                submitted_at=today,
                status="submitted",
                content="Python project submitted successfully.",
            ),
            AssignmentSubmission(
                assignment_id=python_assignment.id,
                student_id=students[1].id,
                submitted_at=today - timedelta(days=1),
                status="submitted",
                content="CLI learning dashboard completed.",
            ),
            AssignmentSubmission(
                assignment_id=python_assignment.id,
                student_id=students[2].id,
                submitted_at=today - timedelta(days=2),
                status="submitted",
                content="Python mini project submitted.",
            ),
            AssignmentSubmission(
                assignment_id=database_assignment.id,
                student_id=students[0].id,
                submitted_at=today - timedelta(days=1),
                status="submitted",
                content="Database design and SQL queries submitted.",
            ),
            AssignmentSubmission(
                assignment_id=database_assignment.id,
                student_id=students[2].id,
                submitted_at=today,
                status="submitted",
                content="SQL assignment submitted.",
            ),
            AssignmentSubmission(
                assignment_id=web_assignment.id,
                student_id=students[1].id,
                submitted_at=today,
                status="submitted",
                content="Full-stack project submitted.",
            ),
        ]

        db.add_all(submissions)
        db.commit()

        # =========================================================
        # TIMETABLE
        # =========================================================

        timetable_entries = [
            Timetable(
                subject_id=subjects[0].id,
                teacher_id=teacher.id,
                day_of_week="Monday",
                start_time="09:00",
                end_time="10:30",
                room="A-201",
            ),
            Timetable(
                subject_id=subjects[1].id,
                teacher_id=teacher.id,
                day_of_week="Wednesday",
                start_time="11:00",
                end_time="12:30",
                room="B-104",
            ),
            Timetable(
                subject_id=subjects[2].id,
                teacher_id=teacher.id,
                day_of_week="Friday",
                start_time="14:00",
                end_time="15:30",
                room="C-302",
            ),
        ]

        db.add_all(timetable_entries)
        db.commit()

        # =========================================================
        # ANNOUNCEMENTS
        # =========================================================

        announcements = [
            Announcement(
                teacher_id=teacher.id,
                subject_id=subjects[0].id,
                title="Mid-semester update",
                message=(
                    "Please complete the Python lab sheets "
                    "before Friday."
                ),
            ),
            Announcement(
                teacher_id=teacher.id,
                subject_id=subjects[1].id,
                title="Database Assignment",
                message=(
                    "The SQL database design assignment "
                    "is now available."
                ),
            ),
            Announcement(
                teacher_id=teacher.id,
                subject_id=subjects[2].id,
                title="Web Development Project",
                message=(
                    "Please submit your full-stack project "
                    "before the deadline."
                ),
            ),
            Announcement(
                teacher_id=teacher.id,
                subject_id=None,
                title="Campus Event",
                message=(
                    "Hackathon registrations are open "
                    "for all departments."
                ),
            ),
        ]

        db.add_all(announcements)
        db.commit()

        print("=" * 60)
        print("DATABASE SEEDED SUCCESSFULLY")
        print("=" * 60)

        print("\nTeacher Login:")
        print("  Email: teacher@example.com")
        print("  Username: teacher")
        print("  Password: teacher123")

        print("\nStudent Logins:")
        print("  1. student@example.com / student123")
        print("  2. priya@example.com / student123")
        print("  3. arjun@example.com / student123")
        print("  4. neha@example.com / student123")
        print("  5. vijay@example.com / student123")

        print("\nStudents Created: 5")
        print("Subjects Created: 3")
        print("Enrollments Created: 15")
        print("Attendance records created for all students.")
        print("Marks created for all students.")
        print("Assignments and submissions created.")
        print("Timetable and announcements created.")
        print("=" * 60)

    except Exception as exc:
        db.rollback()
        print(f"Database seeding failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()