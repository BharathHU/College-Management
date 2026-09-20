# Interview Preparation

## Explain the architecture

Describe the React SPA, FastAPI routers, dependency-based JWT authorization, SQLAlchemy relationships, and the SQLite-to-MySQL configuration boundary. Emphasize that role checks happen on the server.

## Explain the data model

Start with User and the one-to-one profile tables. Then explain the many-to-many relationships: students to subjects through enrollments and teachers to subjects through teacher-subject links. Attendance, marks, assignments, and submissions attach academic activity to those relationships.

## Explain validation and integrity

Pydantic rejects malformed mutation payloads before business logic. Mark ranges are bounded by assessment component, attendance status is enumerated, teacher ownership is checked, and the database uniqueness constraint prevents duplicate attendance.

## Explain trade-offs

Startup bootstrap makes evaluation easy, but production needs migrations. Local storage keeps the demo frontend simple, but production should use a stronger token strategy. Pagination exists on potentially larger subject and student listings; further endpoints can adopt the same envelope as data volume grows.

## Demo walkthrough

Use the student account to show dashboard analytics, profile, subjects, attendance, grades, assignments, timetable, and announcements. Use the teacher account to show assigned subjects, scoped roster, performance, assignment management, and teacher-only mutation APIs. Demonstrate a rejected cross-role request and duplicate attendance response.

Teacher attendance, marks, assignment, and announcement forms use populated assigned-subject and enrolled-student selectors. Assignment review demonstrates content, timing, late detection, and status updates; numeric academic results remain in the marks workflow.

## Likely follow-ups

- How would you add refresh-token rotation?
- How would you migrate from SQLite to MySQL safely?
- How would you audit grade changes?
- How would you test a teacher with two departments and many subjects?
- How would you add notification delivery without coupling it to request latency?