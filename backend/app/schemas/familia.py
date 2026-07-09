from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.familia import (
    EstadoFicha,
    CuadranteKraljic,
    STATUS_DEFAULT,
    CLASIFICACION_PROVEEDORES_DEFAULT,
    CLASIFICACION_CLIENTE_INTERNO_DEFAULT,
)


class StatusBlock(BaseModel):
    spend_2025: float = 0
    num_proveedores: int = 0
    spend_under_control: float = 0
    num_proveedores_suc: int = 0


class ClasificacionProveedoresBlock(BaseModel):
    estrategicos: list[str] = Field(default_factory=list)
    clave: list[str] = Field(default_factory=list)
    tacticos: list[str] = Field(default_factory=list)


class ClienteInternoItem(BaseModel):
    spend: float = 0
    ocs: int = 0


class ClasificacionClienteInternoBlock(BaseModel):
    estrategicos: ClienteInternoItem = Field(default_factory=ClienteInternoItem)
    clave: ClienteInternoItem = Field(default_factory=ClienteInternoItem)
    tacticos: ClienteInternoItem = Field(default_factory=ClienteInternoItem)


class FamiliaBase(BaseModel):
    linea_abastecimiento: str
    descripcion_familia: str = ""
    lider: str = ""
    status: StatusBlock = Field(default_factory=lambda: StatusBlock(**STATUS_DEFAULT))
    analisis_dofa: str = ""
    factores_relevantes: str = ""
    clasificacion_proveedores: ClasificacionProveedoresBlock = Field(
        default_factory=lambda: ClasificacionProveedoresBlock(**CLASIFICACION_PROVEEDORES_DEFAULT)
    )
    kraljic: CuadranteKraljic | None = None
    actores_principales: str = ""
    premisas_negociacion: str = ""
    clasificacion_cliente_interno: ClasificacionClienteInternoBlock = Field(
        default_factory=lambda: ClasificacionClienteInternoBlock(
            **CLASIFICACION_CLIENTE_INTERNO_DEFAULT
        )
    )
    subfamilias: str = ""
    estrategia_aplicar: str = ""
    estado: EstadoFicha = EstadoFicha.BORRADOR


class FamiliaCreate(FamiliaBase):
    pass


class FamiliaUpdate(BaseModel):
    linea_abastecimiento: str | None = None
    descripcion_familia: str | None = None
    lider: str | None = None
    status: StatusBlock | None = None
    analisis_dofa: str | None = None
    factores_relevantes: str | None = None
    clasificacion_proveedores: ClasificacionProveedoresBlock | None = None
    kraljic: CuadranteKraljic | None = None
    actores_principales: str | None = None
    premisas_negociacion: str | None = None
    clasificacion_cliente_interno: ClasificacionClienteInternoBlock | None = None
    subfamilias: str | None = None
    estrategia_aplicar: str | None = None
    estado: EstadoFicha | None = None


class FamiliaOut(FamiliaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    created_by_id: int
    creador_nombre: str = ""
    modificador_nombre: str | None = None


class FamiliaListItem(BaseModel):
    """Version resumida para la tabla de listado."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    linea_abastecimiento: str
    lider: str
    kraljic: CuadranteKraljic | None
    estado: EstadoFicha
    created_at: datetime
    updated_at: datetime
    creador_nombre: str = ""


class FamiliaListResponse(BaseModel):
    items: list[FamiliaListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
