# Security

Passwords are hashed with bcrypt and never returned by the API. JWTs are signed with the configured algorithm and secret, and inactive users are rejected. Endpoint dependencies enforce student/teacher roles and teacher ownership of subjects, assignments, attendance, marks, and announcements.

Request schemas validate credential length, date formats, required text, attendance status, and mark ranges. The database also protects attendance and other relationships with uniqueness constraints.

Production requirements include a high-entropy secret outside source control, HTTPS, restrictive CORS, secure token storage, rate limiting on login, audit logging for grade and attendance changes, dependency scanning, and a migration process. The demo frontend uses local storage for its bearer token; a production client should evaluate secure cookie or equivalent session handling against its deployment threat model.