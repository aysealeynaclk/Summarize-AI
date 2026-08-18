from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, Status, User
from app.schemas import LoginRequest, RegisterRequest, Token, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
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
        role=Role.user,
        status=Status.pending,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username_or_email == payload.username_or_email
    ).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı/e-posta veya şifre hatalı.",
        )

    if user.status == Status.pending:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesabınız onay bekliyor, lütfen yönetici onayını bekleyin.",
        )

    if user.status == Status.inactive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesabınız pasif durumda, lütfen yönetici ile iletişime geçin.",
        )

    token = create_access_token(subject=str(user.id), role=user.role.value)
    return Token(access_token=token, role=user.role)
