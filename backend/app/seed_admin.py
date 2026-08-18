from sqlalchemy.orm import Session

from app.config import settings
from app.models import Role, Status, User
from app.security import hash_password


def seed_admin(db: Session) -> None:
    existing = db.query(User).filter(
        User.username_or_email == settings.admin_username_or_email
    ).first()
    if existing:
        return

    admin = User(
        username_or_email=settings.admin_username_or_email,
        password_hash=hash_password(settings.admin_password),
        role=Role.admin,
        status=Status.active,
    )
    db.add(admin)
    db.commit()
