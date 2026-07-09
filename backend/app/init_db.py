"""
Script de inicializacion de la base de datos.

Crea las tablas (si no existen) y un usuario administrador inicial,
usando las credenciales definidas en las variables de entorno
FIRST_ADMIN_EMAIL / FIRST_ADMIN_PASSWORD / FIRST_ADMIN_NOMBRE.

Uso:
    python -m app.init_db
"""
from sqlalchemy import select

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.user import User, RolUsuario
from app.models import familia  # noqa: F401  (asegura que el modelo se registre en Base)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.scalar(select(User).where(User.email == settings.FIRST_ADMIN_EMAIL))
        if existing:
            print(f"El usuario administrador '{settings.FIRST_ADMIN_EMAIL}' ya existe. No se crea de nuevo.")
            return

        admin = User(
            email=settings.FIRST_ADMIN_EMAIL,
            nombre=settings.FIRST_ADMIN_NOMBRE,
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            rol=RolUsuario.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"Usuario administrador creado: {settings.FIRST_ADMIN_EMAIL}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
