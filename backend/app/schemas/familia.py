from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.familia import (
    EstadoFicha,
    CuadranteKraljic,
    STATUS_DEFAULT,
    ANALISIS_INTERNO_DEFAULT,
    SERIE_ANUAL_DEFAULT,
    CLASIFICACION_PROVEEDORES_DEFAULT,
    CLASIFICACION_CLIENTE_INTERNO_DEFAULT,
    DOFA_DEFAULT,
    FACTORES_RELEVANTES_DEFAULT,
    PODER_NEGOCIACION_DEFAULT,
)

NivelPoderLiteral = Literal["bajo", "alto"]


class StatusBlock(BaseModel):
    num_proveedores: int = 0
    num_ocs: int = 0


class SerieAnualBlock(BaseModel):
    """Serie de 3 valores: año anterior, año actual, año siguiente."""

    y_menos_1: float = 0
    y: float = 0
    y_mas_1: float = 0


class AnalisisInternoBlock(BaseModel):
    spend: SerieAnualBlock = Field(default_factory=lambda: SerieAnualBlock(**SERIE_ANUAL_DEFAULT))
    pct_cobertura: SerieAnualBlock = Field(
        default_factory=lambda: SerieAnualBlock(**SERIE_ANUAL_DEFAULT)
    )
    spend_under_control: SerieAnualBlock = Field(
        default_factory=lambda: SerieAnualBlock(**SERIE_ANUAL_DEFAULT)
    )


class ClasificacionProveedoresBlock(BaseModel):
    apalancados: list[str] = Field(default_factory=list)
    estrategicos: list[str] = Field(default_factory=list)
    rutinarios: list[str] = Field(default_factory=list)
    cuello_de_botella: list[str] = Field(default_factory=list)


class ClienteInternoItem(BaseModel):
    spend: float = 0
    ocs: int = 0


class ClasificacionClienteInternoBlock(BaseModel):
    recurrentes: ClienteInternoItem = Field(default_factory=ClienteInternoItem)
    ocasionales: ClienteInternoItem = Field(default_factory=ClienteInternoItem)


class DofaBlock(BaseModel):
    debilidades: str = ""
    fortalezas: str = ""
    oportunidades: str = ""
    amenazas: str = ""


class FactoresRelevantesBlock(BaseModel):
    insights: str = ""
    indicadores_economicos_financieros: str = ""


class PoderNegociacionBlock(BaseModel):
    veolia: NivelPoderLiteral | None = None
    proveedor: NivelPoderLiteral | None = None


class FamiliaBase(BaseModel):
    linea_abastecimiento: str
    descripcion_familia: str = ""
    lider: str = ""
    status: StatusBlock = Field(default_factory=lambda: StatusBlock(**STATUS_DEFAULT))
    analisis_interno: AnalisisInternoBlock = Field(
        default_factory=lambda: AnalisisInternoBlock(**ANALISIS_INTERNO_DEFAULT)
    )
    analisis_dofa: DofaBlock = Field(default_factory=lambda: DofaBlock(**DOFA_DEFAULT))
    factores_relevantes: FactoresRelevantesBlock = Field(
        default_factory=lambda: FactoresRelevantesBlock(**FACTORES_RELEVANTES_DEFAULT)
    )
    clasificacion_proveedores: ClasificacionProveedoresBlock = Field(
        default_factory=lambda: ClasificacionProveedoresBlock(**CLASIFICACION_PROVEEDORES_DEFAULT)
    )
    kraljic: CuadranteKraljic | None = None
    poder_negociacion: PoderNegociacionBlock = Field(
        default_factory=lambda: PoderNegociacionBlock(**PODER_NEGOCIACION_DEFAULT)
    )
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
    analisis_interno: AnalisisInternoBlock | None = None
    analisis_dofa: DofaBlock | None = None
    factores_relevantes: FactoresRelevantesBlock | None = None
    clasificacion_proveedores: ClasificacionProveedoresBlock | None = None
    kraljic: CuadranteKraljic | None = None
    poder_negociacion: PoderNegociacionBlock | None = None
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