from sqlalchemy.orm import Session

from app.models.revision_estrategica import RevisionEstrategica
from app.models.user import User
from app.schemas.revision_estrategica import RevisionEstrategicaUpdate

# Bloques JSONB que se serializan explicitamente desde sus sub-modelos Pydantic
JSON_BLOCK_FIELDS = (
    "ejes_estrategicos",
    "roadmap",
    "beneficios_esperados",
)


def _attach_nombres(revision: RevisionEstrategica) -> RevisionEstrategica:
    """Adjunta los nombres de creador/modificador como atributos dinamicos para la respuesta."""
    revision.creador_nombre = revision.creador.nombre if revision.creador else ""
    revision.modificador_nombre = revision.modificador.nombre if revision.modificador else None
    return revision


def get_or_create_revision(
    db: Session, familia_id: int, current_user: User
) -> RevisionEstrategica:
    """Obtiene la revision estrategica de una ficha; la crea vacia si aun no existe."""
    revision = db.query(RevisionEstrategica).filter_by(familia_id=familia_id).one_or_none()
    if revision is None:
        revision = RevisionEstrategica(familia_id=familia_id, created_by_id=current_user.id)
        db.add(revision)
        db.commit()
        db.refresh(revision)
    return _attach_nombres(revision)


def update_revision(
    db: Session,
    revision: RevisionEstrategica,
    data: RevisionEstrategicaUpdate,
    current_user: User,
) -> RevisionEstrategica:
    update_data = data.model_dump(exclude_unset=True)

    for field in JSON_BLOCK_FIELDS:
        if field in update_data and update_data[field] is not None:
            update_data[field] = getattr(data, field).model_dump(by_alias=True)

    for key, value in update_data.items():
        setattr(revision, key, value)

    revision.updated_by_id = current_user.id
    db.commit()
    db.refresh(revision)
    return _attach_nombres(revision)