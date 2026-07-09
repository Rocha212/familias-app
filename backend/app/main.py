from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import auth, familias, dashboard, users

# Crea las tablas si no existen (para un setup simple sin migraciones).
# En un entorno de produccion maduro, reemplazar por Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API REST para la gestion de fichas de estandarizacion de familias de abastecimiento.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(familias.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)


@app.get("/api/v1/health", tags=["Salud"])
def health_check():
    """Endpoint simple para verificar que la API esta activa (util para Docker healthcheck)."""
    return {"status": "ok"}
