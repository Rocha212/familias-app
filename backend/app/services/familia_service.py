from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models.familia import Familia, EstadoFicha, CuadranteKraljic
from app.models.user import User
from app.schemas.familia import FamiliaCreate, FamiliaUpdate


def _attach_nombres(db: Session, familia: Familia) -> Familia:
    """Adjunta los nombres de creador/modificador como atributos dinamicos para la respuesta."""
    familia.creador_nombre = familia.creador.nombre if familia.creador else ""
    familia.modificador_nombre = familia.modificador.nombre if familia.modificador else None
    return familia


def get_familia(db: Session, familia_id: int) -> Familia | None:
    familia = db.get(Familia, familia_id)
    if familia:
        _attach_nombres(db, familia)
    return familia


def list_familias(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    estado: EstadoFicha | None = None,
    kraljic: CuadranteKraljic | None = None,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
) -> tuple[list[Familia], int]:
    """Lista fichas con busqueda, filtros, orden y paginacion."""
    query = select(Familia)

    if search:
        like_term = f"%{search}%"
        query = query.where(
            or_(
                Familia.linea_abastecimiento.ilike(like_term),
                Familia.lider.ilike(like_term),
                Familia.descripcion_familia.ilike(like_term),
            )
        )

    if estado:
        query = query.where(Familia.estado == estado)

    if kraljic:
        query = query.where(Familia.kraljic == kraljic)

    count_query = select(func.count()).select_from(query.subquery())
    total = db.scalar(count_query) or 0

    sortable_columns = {
        "linea_abastecimiento": Familia.linea_abastecimiento,
        "lider": Familia.lider,
        "estado": Familia.estado,
        "created_at": Familia.created_at,
        "updated_at": Familia.updated_at,
    }
    sort_column = sortable_columns.get(sort_by, Familia.created_at)
    query = query.order_by(sort_column.desc() if sort_dir == "desc" else sort_column.asc())

    query = query.offset((page - 1) * page_size).limit(page_size)
    familias = list(db.scalars(query).all())
    for familia in familias:
        _attach_nombres(db, familia)

    return familias, total


def create_familia(db: Session, data: FamiliaCreate, current_user: User) -> Familia:
    payload = data.model_dump()
    payload["status"] = data.status.model_dump()
    payload["clasificacion_proveedores"] = data.clasificacion_proveedores.model_dump()
    payload["clasificacion_cliente_interno"] = data.clasificacion_cliente_interno.model_dump()

    familia = Familia(**payload, created_by_id=current_user.id)
    db.add(familia)
    db.commit()
    db.refresh(familia)
    return _attach_nombres(db, familia)


def update_familia(
    db: Session, familia: Familia, data: FamiliaUpdate, current_user: User
) -> Familia:
    update_data = data.model_dump(exclude_unset=True)

    for field in ("status", "clasificacion_proveedores", "clasificacion_cliente_interno"):
        if field in update_data and update_data[field] is not None:
            update_data[field] = getattr(data, field).model_dump()

    for key, value in update_data.items():
        setattr(familia, key, value)

    familia.updated_by_id = current_user.id
    db.commit()
    db.refresh(familia)
    return _attach_nombres(db, familia)


def delete_familia(db: Session, familia: Familia) -> None:
    db.delete(familia)
    db.commit()


def duplicate_familia(db: Session, familia: Familia, current_user: User) -> Familia:
    """Crea una copia de la ficha en estado Borrador, lista para editar."""
    nueva = Familia(
        linea_abastecimiento=f"{familia.linea_abastecimiento} (copia)",
        descripcion_familia=familia.descripcion_familia,
        lider=familia.lider,
        status=dict(familia.status),
        analisis_dofa=familia.analisis_dofa,
        factores_relevantes=familia.factores_relevantes,
        clasificacion_proveedores=dict(familia.clasificacion_proveedores),
        kraljic=familia.kraljic,
        actores_principales=familia.actores_principales,
        premisas_negociacion=familia.premisas_negociacion,
        clasificacion_cliente_interno=dict(familia.clasificacion_cliente_interno),
        subfamilias=familia.subfamilias,
        estrategia_aplicar=familia.estrategia_aplicar,
        estado=EstadoFicha.BORRADOR,
        created_by_id=current_user.id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return _attach_nombres(db, nueva)
