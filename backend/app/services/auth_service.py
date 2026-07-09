from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password, hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Valida credenciales de login. Devuelve el usuario si son correctas."""
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, data: UserCreate) -> User:
    user = User(
        email=data.email,
        nombre=data.nombre,
        rol=data.rol,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))
