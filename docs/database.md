# Database

The relational model contains users, departments, students, teachers, subjects, teacher-subject links, enrollments, attendance, marks, assignments, assignment submissions, timetable entries, and announcements. MySQL is accessed through SQLAlchemy's `mysql+pymysql` dialect.

Important relationships:

- A user has one student or teacher profile.
- Students enroll in subjects through `enrollments`.
- Teachers manage subjects through `teacher_subjects`.
- Attendance and marks reference both a student and subject.
- Assignments belong to a teacher and subject; submissions belong to an assignment and student.
- Announcements belong to a teacher and optionally a subject.

Unique constraints prevent duplicate enrollments, marks per student/subject, attendance for a student/subject/date, and submissions per assignment/student. Indexed identifiers include user email/username, student ID, teacher ID, subject code, and attendance date.

Alembic owns schema creation and evolution. Apply the initial schema with `alembic upgrade head`, then run `python -m app.seed` to create demo records. FastAPI startup does not call `Base.metadata.create_all()`; this prevents application startup from silently changing a production schema. Future model changes require a reviewed Alembic revision.

## Fresh database setup

1. Create an empty MySQL database and application user.
2. Set `DATABASE_URL` to `mysql+pymysql://<user>:<password>@<host>:<port>/<database>`.
3. Run `alembic upgrade head`.
4. Run `python -m app.seed` when demo data is desired.

Do not place real database credentials in source control or documentation.