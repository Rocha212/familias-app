from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.familia import Familia, EstadoFicha
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, ConteoPorCategoria
from app.services import familia_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Datos agregados para el panel principal: totales, ultimas fichas y distribuciones."""
    total_fichas = db.scalar(select(func.count()).select_from(Familia)) or 0

    def contar_estado(estado: EstadoFicha) -> int:
        return db.scalar(
            select(func.count()).select_from(Familia).where(Familia.estado == estado)
        ) or 0

    ultimas_fichas, _ = familia_service.list_familias(
        db, page=1, page_size=5, sort_by="created_at", sort_dir="desc"
    )

    distribucion_kraljic_rows = db.execute(
        select(Familia.kraljic, func.count()).group_by(Familia.kraljic)
    ).all()
    distribucion_kraljic = [
        ConteoPorCategoria(categoria=(k.value if k else "Sin definir"), total=total)
        for k, total in distribucion_kraljic_rows
    ]

    distribucion_estado_rows = db.execute(
        select(Familia.estado, func.count()).group_by(Familia.estado)
    ).all()
    distribucion_estado = [
        ConteoPorCategoria(categoria=estado.value, total=total)
        for estado, total in distribucion_estado_rows
    ]

    return DashboardResponse(
        total_fichas=total_fichas,
        fichas_activas=contar_estado(EstadoFicha.ACTIVA),
        fichas_borrador=contar_estado(EstadoFicha.BORRADOR),
        fichas_archivadas=contar_estado(EstadoFicha.ARCHIVADA),
        ultimas_fichas=ultimas_fichas,
        distribucion_kraljic=distribucion_kraljic,
        distribucion_estado=distribucion_estado,
    )
