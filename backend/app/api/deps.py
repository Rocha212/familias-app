from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, RolUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Resuelve el usuario autenticado a partir del JWT enviado en el header Authorization."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = db.get(User, int(user_id))
    if user is None or not user.is_active:
        raise credentials_error

    return user


def require_roles(*allowed_roles: RolUsuario):
    """Fabrica de dependencias para restringir un endpoint a ciertos roles."""

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para esta accion",
            )
        return current_user

    return checker


# Atajos comunes de autorizacion
require_admin = require_roles(RolUsuario.ADMIN)
require_editor = require_roles(RolUsuario.ADMIN, RolUsuario.EDITOR)
require_any_authenticated = get_current_user
