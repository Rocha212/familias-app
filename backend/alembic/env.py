import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Permite importar el paquete "app" al correr alembic desde backend/
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.core.database import Base

# Importa aqui todos los modulos de modelos para que se registren en Base.metadata
from app.models import familia  # noqa: F401
from app.models import user  # noqa: F401

from app.models import revision_estrategica  # noqa: F401

config = context.config

# Inyecta la URL real de la base de datos (desde variables de entorno / .env)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()