import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, require_editor, require_admin
from app.models.familia import Familia, EstadoFicha, CuadranteKraljic
from app.models.user import User
from app.schemas.familia import (
    FamiliaCreate,
    FamiliaUpdate,
    FamiliaOut,
    FamiliaListResponse,
)
from app.services import familia_service
from app.services.pdf_service import generate_familia_pdf

router = APIRouter(prefix="/familias", tags=["Fichas de Familias"])


def _get_or_404(db: Session, familia_id: int) -> Familia:
    familia = familia_service.get_familia(db, familia_id)
    if not familia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ficha no encontrada")
    return familia


@router.get("", response_model=FamiliaListResponse)
def list_familias(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    estado: EstadoFicha | None = Query(None),
    kraljic: CuadranteKraljic | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista fichas con busqueda, filtros, orden y paginacion para la tabla principal."""
    familias, total = familia_service.list_familias(
        db, page, page_size, search, estado, kraljic, sort_by, sort_dir
    )
    total_pages = max(1, math.ceil(total / page_size))
    return FamiliaListResponse(
        items=familias, total=total, page=page, page_size=page_size, total_pages=total_pages
    )


@router.get("/{familia_id}", response_model=FamiliaOut)
def get_familia(
    familia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_or_404(db, familia_id)


@router.post("", response_model=FamiliaOut, status_code=status.HTTP_201_CREATED)
def create_familia(
    payload: FamiliaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    return familia_service.create_familia(db, payload, current_user)


@router.put("/{familia_id}", response_model=FamiliaOut)
def update_familia(
    familia_id: int,
    payload: FamiliaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    familia = _get_or_404(db, familia_id)
    return familia_service.update_familia(db, familia, payload, current_user)


@router.delete("/{familia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_familia(
    familia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    familia = _get_or_404(db, familia_id)
    familia_service.delete_familia(db, familia)
    return None


@router.post("/{familia_id}/duplicar", response_model=FamiliaOut, status_code=status.HTTP_201_CREATED)
def duplicate_familia(
    familia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_editor),
):
    familia = _get_or_404(db, familia_id)
    return familia_service.duplicate_familia(db, familia, current_user)


@router.get("/{familia_id}/pdf")
def export_familia_pdf(
    familia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Genera y descarga el PDF de la ficha, replicando el formato visual oficial."""
    familia = _get_or_404(db, familia_id)
    pdf_bytes = generate_familia_pdf(familia)
    filename = f"ficha_{familia.id}_{familia.linea_abastecimiento[:30].replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
