from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import RoleEnum, Student, Teacher, User
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    username = payload.username
    password = payload.password

    user = db.query(User).filter((User.email == username) | (User.username == username)).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.id, timedelta(minutes=settings.access_token_expire_minutes))

    profile = None
    if user.role == RoleEnum.STUDENT:
        student = db.query(Student).filter(Student.user_id == user.id).first()
        profile = {"student_id": student.student_id if student else None}
    elif user.role == RoleEnum.TEACHER:
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        profile = {"teacher_id": teacher.teacher_id if teacher else None}

    return {
        "success": True,
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": {"id": user.id, "email": user.email, "username": user.username, "role": user.role.value, **profile},
        },
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "role": current_user.role.value,
        },
    }


@router.post("/logout")
def logout():
    return {"success": True, "data": {"message": "Logged out successfully"}}
