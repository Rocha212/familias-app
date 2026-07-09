from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import RolUsuario


class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    rol: RolUsuario = RolUsuario.LECTOR


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nombre: str | None = None
    rol: RolUsuario | None = None
    is_active: bool | None = None
    password: str | None = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
