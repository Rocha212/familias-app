from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_editor
from app.models.user import User
from app.schemas.revision_estrategica import RevisionEstrategicaOut, RevisionEstrategicaUpdate
from app.services import familia_service, revision_service

router = APIRouter(prefix="/familias/{familia_id}/revision", tags=["Revision Estrategica"])


def _get_familia_or_404(db: Session, familia_id: int):
    familia = familia_service.get_familia(db, familia_id)
    if not familia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ficha no encontrada")
    return familia


@router.get("", response_model=RevisionEstrategicaOut)
def get_revision(
    familia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Obtiene las paginas 2 y 3 de la ficha (Donde queremos llegar / Que resultados esperamos).

    Se crea automaticamente vacia la primera vez que se consulta.
    """
    _get_familia_or_404(db, familia_id)
    return revision_service.get_or_create_revision(db, familia_id, current_user)


@router.put("", response_model=RevisionEstrategicaOut)
def update_revision(
    familia_id: int,
    payload: RevisionEstrategicaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    """Actualiza las paginas 2 y 3 de la ficha."""
    _get_familia_or_404(db, familia_id)
    revision = revision_service.get_or_create_revision(db, familia_id, current_user)
    return revision_service.update_revision(db, revision, payload, current_user)