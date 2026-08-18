from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models import AILog, Role, User
from app.schemas import (
    AdminCreateUserRequest,
    AdminUpdateUserRequest,
    LogOut,
    UserOut,
)
from app.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/logs", response_model=list[LogOut])
def list_logs(db: Session = Depends(get_db)):
    logs = db.query(AILog).order_by(AILog.created_at.desc()).all()
    result = []
    for log in logs:
        item = LogOut.model_validate(log)
        item.username_or_email = log.user.username_or_email
        result.append(item)
    return result


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: AdminCreateUserRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        User.username_or_email == payload.username_or_email
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu kullanıcı adı/e-posta zaten kayıtlı.",
        )

    user = User(
        username_or_email=payload.username_or_email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        status=payload.status,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: AdminUpdateUserRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı.",
        )

    if payload.status is not None:
        user.status = payload.status

    if payload.new_password:
        user.password_hash = hash_password(payload.new_password)

    db.commit()
    db.refresh(user)
    return user
