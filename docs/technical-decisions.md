# Technical Decisions

## FastAPI, SQLAlchemy, and MySQL

FastAPI provides typed request validation and OpenAPI generation. SQLAlchemy provides the existing relational model and uses PyMySQL for MySQL connectivity.

## React and Vite

React provides reusable portal components and Vite keeps local iteration and production builds fast. Recharts is used for dashboard visualizations.

## JWT and bcrypt

JWT bearer access tokens fit the separate frontend/backend deployment model. Bcrypt is used for password hashing. The current implementation intentionally keeps the existing authentication contract stable.

## Alembic migrations

Alembic is the production schema authority. The initial migration captures the current tables, relationships, indexes, and constraints. FastAPI startup does not create tables; operators run `alembic upgrade head` explicitly, followed by the optional idempotent seed command.

## Scope enforcement

Teacher ownership is checked against teacher-subject links before attendance, marks, assignments, or subject announcements are changed. This is more important than relying on navigation visibility, because the backend is the final security boundary.

## Assignment review boundary

Assignment submissions retain content, submission time, late detection, and workflow status. Numeric grades and feedback are intentionally not duplicated in submissions because the application already has a marks and grades domain. Teachers can update submission status while academic marks remain managed through the marks endpoint.

## Frontend bundle advisory

Recharts remains part of the dashboard because the charts are a required product feature. The chart module is lazy-loaded, reducing the initial JavaScript bundle; further code splitting can be considered if the application grows.