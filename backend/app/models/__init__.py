"""
Importa aqui todos los modelos ORM para que SQLAlchemy los registre en Base.metadata
y pueda resolver relaciones referenciadas por nombre (string) entre modelos,
sin importar desde que punto de la aplicacion se importe primero "app.models".
"""
from app.models.user import User  # noqa: F401
from app.models.familia import Familia  # noqa: F401
from app.models.revision_estrategica import RevisionEstrategica  # noqa: F401