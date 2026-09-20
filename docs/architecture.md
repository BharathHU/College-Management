# Architecture

The system is a two-tier web application:

- `frontend/`: React 19 and Vite single-page portal with role-aware navigation.
- `backend/`: FastAPI application exposing JSON APIs.
- Database: MySQL accessed through SQLAlchemy and PyMySQL, with Alembic as the schema authority.

Requests flow through the React API client to FastAPI routers, then through the auth dependency and SQLAlchemy session to MySQL. Schema changes flow separately through Alembic migrations. Student and teacher routers enforce role boundaries at the endpoint, not only in the UI.

## Runtime flow

1. User posts credentials to `/api/auth/login`.
2. FastAPI verifies the bcrypt hash and returns a short-lived JWT.
3. The frontend stores the token locally for this demo and sends it as a bearer token.
4. `get_current_user` validates the token and loads the active user.
5. `require_role` rejects users outside the endpoint's role policy.

## Structure

Routers own HTTP contracts and authorization. Models own persistence relationships and constraints. `app/schemas` owns request validation. `core/security.py` owns password and JWT operations. `backend/alembic` owns schema history and migration execution. This keeps domain behavior reusable without introducing a second service layer prematurely.