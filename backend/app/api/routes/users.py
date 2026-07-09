from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.api.deps import require_admin, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.auth_service import create_user, get_user_by_email

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")
    return create_user(db, payload)


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = payload.model_dump(exclude_unset=True)
    if "password" in data and data["password"]:
        user.hashed_password = hash_password(data.pop("password"))
    else:
        data.pop("password", None)
    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
