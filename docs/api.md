# API

All protected endpoints use `Authorization: Bearer <access_token>` and return `{ "success": true, "data": ... }` on success. Validation failures use FastAPI's 422 response; authentication failures use 401; role or ownership failures use 403; missing records use 404; duplicate attendance uses 409.

## Main routes

- `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`
- `GET /api/dashboard/student`, `GET /api/dashboard/teacher`
- `GET /api/students/me`, `/subjects`, `/attendance`, `/marks`, `/assignments`, `/timetable`, `/announcements`, `/performance`
- `GET /api/teachers/me`, `/subjects`, `/students`, `/performance`
- `POST /api/attendance/mark`
- `POST /api/marks/upsert`
- `GET /api/assignments/student`, `GET /api/assignments/teacher`, `POST /api/assignments/create`
- `POST /api/assignments/{id}/submit`, `GET /api/assignments/{id}/submissions`, `PATCH /api/assignments/{id}/submissions/{submission_id}`
- `GET /api/subjects`, `GET /api/subjects/{id}`
- `GET /api/timetable`, `GET /api/announcements`, `POST /api/announcements/create`

Subject search supports `q`, `department`, `semester`, `page`, and `limit`, including teacher assigned-subject search. Assignment listings support `q`, `status`, `page`, and `limit`. Student attendance and marks support `q`; teacher student roster search supports `subject_id`, `q`, `page`, and `limit`.

Teacher mutation forms populate subjects from the authenticated teacher's assigned-subject endpoint and students from the selected subject roster. The backend still validates ownership for every mutation.

Assignment review currently covers submission content, submitted time, late status, and workflow status (`submitted`, `graded`, or `missing`). Numeric grades and feedback remain in the existing marks/grades workflow rather than being duplicated on assignment submissions.