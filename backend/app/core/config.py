from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion central de la aplicacion, leida desde variables de entorno."""

    PROJECT_NAME: str = "Gestion de Fichas de Estandarizacion"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/fichas_db"

    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 horas

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:3000",
        "http://localhost",
    ]

    FIRST_ADMIN_EMAIL: str = "admin@empresa.com"
    FIRST_ADMIN_PASSWORD: str = "Admin123!"
    FIRST_ADMIN_NOMBRE: str = "Administrador"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
