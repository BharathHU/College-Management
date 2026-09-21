# 🎓 College Management System

> A modern full-stack college portal built with **React, FastAPI, MySQL, and JWT authentication**, providing separate workflows for students and teachers with role-based access, dashboard analytics, API validation, and production-oriented database migrations.

![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge\&logo=react\&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-7+-646CFF?style=for-the-badge\&logo=vite\&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3+-06B6D4?style=for-the-badge\&logo=tailwindcss\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8+-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA81E?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge\&logo=jsonwebtokens)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Overview

The **College Management System** is a full-stack web application designed to digitize common academic and administrative workflows.

The application provides dedicated experiences for **students and teachers**, while the backend enforces authentication, authorization, validation, and database integrity.

### ✨ Key Highlights

* 👨‍🎓 Student and teacher workflows
* 🔐 JWT-based authentication
* 🛡️ Role-based access control
* 🔑 Bcrypt password hashing
* 📊 Dashboard analytics with Recharts
* 🚀 RESTful APIs using FastAPI
* 🗄️ MySQL relational database
* 🔄 Alembic database migrations
* ✅ Pydantic request/response validation
* ⚡ React + Vite frontend
* 🎨 Tailwind CSS UI
* 🧪 Backend API testing with Pytest
* 🐳 Docker Compose configuration
* 📚 Interactive Swagger API documentation

---


---

# 📦 Submission & Evaluation Guide

This README is organized to help an evaluator download, configure, run, test, and understand the application without requiring access to private credentials.

## 1. Working Application

The application consists of:

- **Frontend:** React + Vite
- **Backend:** FastAPI
- **Database:** MySQL
- **Authentication:** JWT + Bcrypt

### Local application URLs

```text
Frontend: http://localhost:5173
Backend:  http://localhost:8000
Swagger:  http://localhost:8000/docs
ReDoc:    http://localhost:8000/redoc
```

### Recommended verification flow

```text
Start Database
      ↓
Run Database Migrations
      ↓
Seed Demo Data
      ↓
Start FastAPI Backend
      ↓
Start React Frontend
      ↓
Open Login Page
      ↓
Login with Demo Credentials
      ↓
Test Student / Teacher Workflows
      ↓
Verify Dashboard and API Operations
```

---

# 🗃️ Database Setup & Schema

The project uses **MySQL** with **SQLAlchemy** and **Alembic**.

## Database requirements

Before starting the backend, ensure that:

- MySQL 8+ is installed and running.
- A database named `college_management` is available.
- The `DATABASE_URL` in the environment configuration points to the correct database.

Example:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/college_management
```

## Create / update the schema

Run:

```bash
cd backend
alembic upgrade head
```

Alembic migrations are the source of truth for schema changes.

## Seed demo data

Run:

```bash
python -m app.seed
```

This prepares demo records that can be used to verify the application's workflows.

## Verify the database

After migration and seeding, verify that the expected tables and demo records are present in MySQL.

> Do not commit production credentials, personal database passwords, API keys, or other secrets to the repository.

---

# 🌱 Sample / Demo Data

The project provides seed data for local demonstration.

Demo accounts:

### Student

```text
Email:    student@example.com
Password: student123
Role:     Student
```

### Teacher

```text
Email:    teacher@example.com
Password: teacher123
Role:     Teacher
```

These credentials are intended for local development and assessment/demo purposes only.

If the evaluator resets the database, run:

```bash
python -m app.seed
```

to recreate the supported demo data.

---

# 🔐 Environment Configuration

The repository should contain an example environment configuration, but **must not expose real secrets**.

## Required approach

Create or maintain:

```text
.env.example
```

Example:

```env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/college_management
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

For local development:

```text
.env.example
      ↓
copy to local .env
      ↓
replace placeholder values
      ↓
run application
```

### Windows

```powershell
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

> Never commit the real `.env` file. The `.gitignore` file should exclude it from version control.

---

# 🏗️ Architecture / Design

The application follows a layered full-stack architecture:

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         │   React + Vite      │
                         └──────────┬──────────┘
                                    │
                              HTTP / REST
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │   Backend Server    │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        Authentication       Business Logic        Validation
         JWT + Bcrypt          Services             Pydantic
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                              SQLAlchemy ORM
                                    │
                                    ▼
                               MySQL Database
                                    ▲
                                    │
                               Alembic
                              Migrations
```

The `docs/` directory is intended for supporting architecture/design documentation.

If an architecture image is included in the submission, place it at:

```text
docs/architecture.png
```

---

# 🔄 Application Data Flow

A typical authenticated request follows:

```text
React Component
      ↓
API Service
      ↓
HTTP Request + JWT
      ↓
FastAPI Router
      ↓
JWT Authentication
      ↓
Role Authorization
      ↓
Pydantic Validation
      ↓
Service / Business Logic
      ↓
SQLAlchemy ORM
      ↓
MySQL
      ↓
API Response
      ↓
React State
      ↓
UI Update
```

This separation makes the frontend, API layer, business logic, and persistence layer easier to understand and maintain.

---

# 🧠 Major Technical Decisions

## FastAPI

FastAPI is used for REST API development, request validation, automatic OpenAPI/Swagger documentation, and an ASGI-based backend architecture.

## React + Vite

React provides reusable UI components, while Vite provides the frontend development and build workflow.

## MySQL

MySQL is used because the application manages relational academic data that benefits from structured tables, relationships, constraints, transactions, and indexing.

## SQLAlchemy

SQLAlchemy provides ORM-based database interaction and separates application code from direct SQL execution.

## Pydantic

Pydantic is used for request/response validation and helps ensure that API data follows the expected structure.

## JWT + Bcrypt

JWT is used for authenticated API requests and role-based authorization. Bcrypt is used for password hashing rather than storing plain-text passwords.

## Alembic

Alembic provides version-controlled database migrations so schema changes can be applied consistently across environments.

## Docker Compose

Docker Compose provides a reproducible way to configure and run the application's services when Docker is available.

---

# ⚡ Performance Considerations

Performance is considered at multiple layers.

### Frontend

- Reusable React components reduce duplicated UI logic.
- Vite provides an efficient development/build workflow.
- Data is loaded through APIs instead of coupling the UI directly to the database.
- Dashboard visualizations are rendered from API-driven data.

### Backend

- FastAPI provides an efficient API framework.
- Business logic is separated from routing where applicable.
- Pydantic validation prevents invalid request data from reaching deeper application layers.
- SQLAlchemy provides structured database access.

### Database

- MySQL provides indexed and relational data access.
- Alembic provides controlled schema evolution.
- Queries should retrieve only the data required by each operation.
- Database connections are managed through the application's database layer.

---

# 🔒 Security Decisions

The project includes the following security-related mechanisms:

- JWT authentication
- Bcrypt password hashing
- Role-based authorization
- Protected API endpoints
- Pydantic request validation
- Environment-based secrets
- `.env` excluded from version control
- CORS configuration
- Short-lived JWT strategy

### Security rule for submission

The submission must not contain:

```text
Real database passwords
Real JWT secrets
API keys
Personal access tokens
Private credentials
```

Use `.env.example` with placeholders instead.

---

# 🧪 Application Verification Checklist

Before submitting the project, verify the following:

```text
[ ] MySQL is running
[ ] Database migrations run successfully
[ ] Demo data can be seeded
[ ] Backend starts successfully
[ ] Swagger documentation opens
[ ] Frontend starts successfully
[ ] Student login works
[ ] Teacher login works
[ ] Protected routes work
[ ] Role restrictions work
[ ] Dashboard loads correctly
[ ] Main API operations work
[ ] No real secrets are committed
[ ] README setup instructions work from a clean environment
```

---

# 🖼️ Screenshots / Demonstration Evidence

Screenshots are optional but recommended for the assessment submission.

Recommended screenshots:

```text
screenshots/
├── 01-login.png
├── 02-student-dashboard.png
├── 03-teacher-dashboard.png
├── 04-student-workflow.png
├── 05-teacher-workflow.png
├── 06-api-swagger.png
└── 07-database.png
```

Screenshots should demonstrate the actual working application rather than placeholder UI.

---

# 🎥 Optional Demonstration Video

A short demonstration video can be included as supporting evidence.

Recommended flow:

```text
1. Open the application
2. Login as Student
3. Demonstrate student functionality
4. Logout
5. Login as Teacher
6. Demonstrate teacher functionality
7. Show dashboard analytics
8. Open Swagger API documentation
9. Demonstrate an API operation
10. Briefly show the database/migration setup
```

A short, focused demonstration is sufficient; the video is optional.

---

# 📋 Submission Package Checklist

The final assessment submission should contain:

| Requirement | Submission Item |
|---|---|
| Working application | Frontend + backend that can be run locally |
| Database setup | Alembic migrations and database setup instructions |
| Sample/demo data | `app.seed` / supported seed process and demo accounts |
| README | This document with complete setup and execution instructions |
| Architecture/design | Architecture section + optional `docs/architecture.png` |
| Environment configuration | `.env.example` with placeholders |
| Demo credentials | Student and Teacher demo accounts |
| Technical decisions | Technical Decisions section |
| Screenshots | Optional `screenshots/` directory |
| Demonstration video | Optional short demo video |

> The complete source code is maintained separately as the project repository contents; this README focuses on setup, execution, architecture, configuration, testing, and evaluation information.

---

# 🚦 Clean Evaluation Setup

An evaluator should be able to follow this sequence:

```bash
git clone <your-repository-url>
cd college-management-system
```

Configure the environment:

```text
Create local .env from .env.example
```

Set up the backend:

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Seed demo data:

```bash
python -m app.seed
```

Start backend:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
Frontend: http://localhost:5173
Swagger:  http://localhost:8000/docs
```

Use the demo credentials listed above to verify the application.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         │   React + Vite      │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP / REST API
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │   Backend Server    │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
          │    Auth     │    │   Business  │    │ Validation  │
          │ JWT + Bcrypt│    │    Logic    │    │  Pydantic   │
          └─────────────┘    └──────┬──────┘    └─────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │  SQLAlchemy   │
                            │      ORM      │
                            └───────┬───────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │     MySQL     │
                            │   Database    │
                            └───────────────┘
                                    ▲
                                    │
                            ┌───────┴───────┐
                            │    Alembic    │
                            │   Migrations  │
                            └───────────────┘
```

---

# 🛠️ Tech Stack

## Frontend

| Technology       | Purpose                            |
| ---------------- | ---------------------------------- |
| **React**        | Component-based UI                 |
| **Vite**         | Frontend development/build tooling |
| **Tailwind CSS** | Responsive UI styling              |
| **Recharts**     | Dashboard analytics and charts     |

## Backend

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| **FastAPI**    | REST API framework           |
| **Python**     | Backend programming language |
| **SQLAlchemy** | ORM and database interaction |
| **Pydantic**   | Request/response validation  |
| **PyMySQL**    | MySQL database driver        |
| **JWT**        | Authentication               |
| **Bcrypt**     | Password hashing             |
| **Uvicorn**    | ASGI server                  |

## Database & DevOps

| Technology         | Purpose                    |
| ------------------ | -------------------------- |
| **MySQL**          | Relational database        |
| **Alembic**        | Database schema migrations |
| **Pytest**         | Backend testing            |
| **Docker Compose** | Container orchestration    |
| **Git/GitHub**     | Version control            |

---

# 🚀 Features

## 🔐 Authentication & Authorization

The system implements secure authentication using:

* JWT access tokens
* Bcrypt password hashing
* Role-based authorization
* Protected API endpoints
* Student/Teacher access separation
* Short-lived token strategy

```text
User Login
    │
    ▼
Credentials Validation
    │
    ▼
Password Verification
    │
    ▼
JWT Token Generated
    │
    ▼
Frontend Stores Token
    │
    ▼
Protected API Request
    │
    ▼
Backend Validates JWT
    │
    ▼
Role Authorization
    │
    ▼
Response
```

---

## 👨‍🎓 Student Workflow

Students can access student-specific functionality through authenticated APIs and protected frontend routes.

Typical workflow:

```text
Login
  ↓
Student Dashboard
  ↓
View Academic Information
  ↓
Access Student Features
  ↓
View Dashboard Analytics
```

---

## 👨‍🏫 Teacher Workflow

Teachers have access to teacher-specific functionality based on their authenticated role.

```text
Login
  ↓
Teacher Dashboard
  ↓
Access Teacher Features
  ↓
Manage/View Academic Data
  ↓
Dashboard Analytics
```

---

# 📊 Dashboard Analytics

The frontend uses **Recharts** to visualize application data.

Examples of possible dashboard visualizations include:

* Student statistics
* Teacher statistics
* Academic data
* Distribution charts
* Summary metrics
* Performance-related analytics

Example data flow:

```text
MySQL
  ↓
SQLAlchemy
  ↓
FastAPI Service
  ↓
REST API
  ↓
React
  ↓
Recharts
  ↓
Interactive Dashboard
```

---

# 🗄️ Database Architecture

The application uses **MySQL** as its primary relational database.

SQLAlchemy provides ORM-based interaction between the FastAPI application and MySQL.

```text
FastAPI
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PyMySQL
   │
   ▼
MySQL
```

### Why MySQL?

* Relational data modeling
* Referential integrity
* Transactions
* Indexing
* Mature production ecosystem
* Good compatibility with SQLAlchemy

---

# 🔄 Database Migrations

Database schema changes are managed using **Alembic**.

The application intentionally does **not** use:

```python
Base.metadata.create_all()
```

as a production migration mechanism.

Instead:

```text
SQLAlchemy Models
       │
       ▼
Alembic Autogenerate
       │
       ▼
Migration Review
       │
       ▼
alembic upgrade head
       │
       ▼
MySQL Schema
```

### Create a migration

```bash
alembic revision --autogenerate -m "describe change"
```

### Apply migrations

```bash
alembic upgrade head
```

### Roll back one migration

```bash
alembic downgrade -1
```

---

# 📁 Project Structure

```text
college-management-system/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   ├── auth/
│   │   ├── main.py
│   │   └── seed.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── security.md
│   ├── technical-decisions.md
│   └── interview-preparation.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone <your-repository-url>
cd college-management-system
```

---

## 2️⃣ Configure environment variables

Copy the example environment file:

```bash
cp .env.example backend/.env
```

For Windows:

```powershell
copy .env.example backend\.env
```

Configure your database:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/college_management

SECRET_KEY=your-strong-secret-key

ALGORITHM=HS256
```

> ⚠️ Never commit your real `.env` file to GitHub.

---

# 🐍 Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🗃️ Create Database Schema

Run Alembic migrations:

```bash
alembic upgrade head
```

Seed demo data:

```bash
python -m app.seed
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# ⚛️ Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🧪 Testing

Run backend tests:

```bash
cd backend
python -m pytest
```

Testing covers backend functionality and API behavior.

---

# 👤 Demo Accounts

### Student

```text
Email:    student@example.com
Password: student123
Role:     Student
```

### Teacher

```text
Email:    teacher@example.com
Password: teacher123
Role:     Teacher
```

> These credentials are intended only for local development/demo environments.

---

# 🔌 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

The API follows a REST-based architecture and uses Pydantic schemas for request and response validation.

---

# 🔒 Security

Security considerations implemented in the project include:

* 🔐 JWT authentication
* 🔑 Bcrypt password hashing
* 🛡️ Role-based authorization
* ✅ Pydantic API validation
* 🌐 Restricted CORS configuration
* 🔒 Environment-based secrets
* ⏱️ Short-lived JWT tokens
* 🗄️ Database access through SQLAlchemy
* 🚫 `.env` excluded from version control

### Production security roadmap

Before public deployment, consider adding:

* TLS/HTTPS termination
* Rate limiting
* Refresh-token rotation
* Centralized logging
* Monitoring and alerting
* Health checks
* Managed MySQL
* Automated backups
* Secret management
* Security headers

---

# 🐳 Docker

The project includes Docker Compose configuration.

Validate the Compose configuration:

```bash
docker compose config
```

Build the services:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Expected development ports:

```text
Frontend → 5173
Backend  → 8000
MySQL    → 3306
```

> Docker build/start verification should be performed on a system with Docker Desktop or Docker Engine installed.

---

# 🔁 Application Data Flow

A typical authenticated request follows this flow:

```text
React Component
      │
      ▼
API Service
      │
      ▼
HTTP Request + JWT
      │
      ▼
FastAPI Router
      │
      ▼
JWT Authentication
      │
      ▼
Role Authorization
      │
      ▼
Pydantic Validation
      │
      ▼
Service / Business Logic
      │
      ▼
SQLAlchemy ORM
      │
      ▼
MySQL
      │
      ▼
API Response
      │
      ▼
React State
      │
      ▼
UI Update
```

---

# 🧠 Technical Decisions

### Why FastAPI?

FastAPI was selected because it provides:

* High-performance ASGI support
* Automatic API documentation
* Pydantic validation
* Type-hint-based development
* Clean REST API architecture

### Why React?

React provides:

* Reusable components
* Efficient UI updates
* Component-based architecture
* Strong ecosystem
* Easy integration with REST APIs

### Why SQLAlchemy?

SQLAlchemy provides:

* ORM abstraction
* Reusable database models
* Query construction
* Transaction management
* Database portability

### Why Alembic?

Alembic provides version-controlled database schema changes.

Instead of recreating the database schema, migrations allow controlled evolution:

```text
Version 1
   ↓
Version 2
   ↓
Version 3
   ↓
Version 4
```

---

# ⚡ Performance Considerations

The application considers performance at multiple layers:

### Frontend

* Vite-based development/build process
* Component reuse
* API-driven data loading
* Efficient dashboard rendering

### Backend

* FastAPI asynchronous architecture
* SQLAlchemy ORM
* Database query optimization
* Pydantic validation
* Separation of routing and business logic

### Database

* Relational schema
* Indexed lookup fields where appropriate
* Controlled schema evolution through Alembic
* Connection management

---

# 📚 Documentation

Detailed project documentation is available in the `docs/` directory:

| Document                   | Description                     |
| -------------------------- | ------------------------------- |
| `architecture.md`          | Application architecture        |
| `database.md`              | Database design                 |
| `api.md`                   | API documentation               |
| `security.md`              | Security decisions              |
| `technical-decisions.md`   | Technology/design decisions     |
| `interview-preparation.md` | Technical interview preparation |

---

# 🚀 Future Improvements

Potential future enhancements include:

* 📱 Mobile-responsive improvements
* 🔔 Notification system
* 📧 Email notifications
* 📄 PDF report generation
* 📅 Attendance management
* 📝 Assignment management
* 📚 Course management
* 💬 Student-teacher communication
* 🔄 Refresh-token authentication
* 📈 Advanced analytics
* ☁️ Cloud deployment
* 🔍 Advanced search and filtering

---

# 🎯 Project Highlights

This project demonstrates practical experience with:

```text
Frontend Development
        +
REST API Development
        +
Authentication & Authorization
        +
Database Design
        +
ORM
        +
Database Migrations
        +
API Validation
        +
Dashboard Analytics
        +
Testing
        +
Docker
```

It is designed to demonstrate how a **modern full-stack application** can be structured with clear separation between frontend, backend, authentication, business logic, and database layers.

---


---

# 🎯 Assessment Notes

This project is prepared to support a technical discussion covering:

- Architecture and design
- Technology/library selection
- End-to-end data flow
- Database design and migrations
- Authentication and authorization
- Security decisions
- Performance considerations
- Reusable frontend/backend components
- API design and validation
- Testing approach
- Docker-based execution
- Small live feature modifications during the technical discussion

The evaluator can use the setup, architecture, demo credentials, API documentation, and verification checklist above as the primary guide for running the application.

# 👨‍💻 Developer

**Bharath H U**

Python Full-Stack Developer

### Technologies

```text
Python • FastAPI • Django • React • JavaScript
MySQL • SQLAlchemy • REST APIs • JWT
Tailwind CSS • Git • GitHub • Docker
```

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.

```text
Built with ❤️ using Python + React
```

---
