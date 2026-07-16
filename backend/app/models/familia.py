import enum
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EstadoFicha(str, enum.Enum):
    BORRADOR = "borrador"
    ACTIVA = "activa"
    ARCHIVADA = "archivada"


class CuadranteKraljic(str, enum.Enum):
    ESTRATEGICO = "estrategico"
    CUELLO_DE_BOTELLA = "cuello_de_botella"
    APALANCAMIENTO = "apalancamiento"
    RUTINARIO = "rutinario"


class NivelPoder(str, enum.Enum):
    BAJO = "bajo"
    ALTO = "alto"


# ---------------------------------------------------------------------------
# Estructuras por defecto de los bloques JSON, usadas al crear una ficha nueva
# ---------------------------------------------------------------------------

# Bloque STATUS: conteos simples (no series temporales)
STATUS_DEFAULT = {
    "num_proveedores": 0,
    "num_ocs": 0,
}

# Serie temporal generica Y-1 / Y / Y+1, reutilizada dentro de ANALISIS_INTERNO
SERIE_ANUAL_DEFAULT = {
    "y_menos_1": 0,
    "y": 0,
    "y_mas_1": 0,
}

# Bloque ANALISIS INTERNO: tres metricas, cada una con su serie Y-1/Y/Y+1
ANALISIS_INTERNO_DEFAULT = {
    "spend": dict(SERIE_ANUAL_DEFAULT),
    "pct_cobertura": dict(SERIE_ANUAL_DEFAULT),
    "spend_under_control": dict(SERIE_ANUAL_DEFAULT),
}

# Bloque CLASIFICACION PROVEEDORES: 4 categorias segun matriz Kraljic
CLASIFICACION_PROVEEDORES_DEFAULT = {
    "apalancados": [],
    "estrategicos": [],
    "rutinarios": [],
    "cuello_de_botella": [],
}

# Bloque CLASIFICACION CLIENTE INTERNO: 2 categorias (spend / # OCs)
CLASIFICACION_CLIENTE_INTERNO_DEFAULT = {
    "recurrentes": {"spend": 0, "ocs": 0},
    "ocasionales": {"spend": 0, "ocs": 0},
}

# Bloque ANALISIS DOFA: 4 sub-campos estructurados
DOFA_DEFAULT = {
    "debilidades": "",
    "fortalezas": "",
    "oportunidades": "",
    "amenazas": "",
}

# Bloque FACTORES RELEVANTES: insights + indicadores economicos y financieros
FACTORES_RELEVANTES_DEFAULT = {
    "insights": "",
    "indicadores_economicos_financieros": "",
}

# Bloque PODER DE NEGOCIACION: nivel (bajo/alto) por actor
PODER_NEGOCIACION_DEFAULT = {
    "veolia": None,
    "proveedor": None,
}


class Familia(Base):
    """Ficha de estandarizacion de una familia de abastecimiento (Fase 1 - Pagina 1: Donde estamos)."""

    __tablename__ = "familias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Encabezado
    linea_abastecimiento: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    descripcion_familia: Mapped[str] = mapped_column(Text, default="")
    lider: Mapped[str] = mapped_column(String(150), default="")

    # Bloque STATUS (conteos simples)
    status: Mapped[dict] = mapped_column(JSONB, default=lambda: dict(STATUS_DEFAULT))

    # Bloque ANALISIS INTERNO (series Y-1 / Y / Y+1)
    analisis_interno: Mapped[dict] = mapped_column(
        JSONB, default=lambda: {k: dict(v) for k, v in ANALISIS_INTERNO_DEFAULT.items()}
    )

    # Bloque ANALISIS DOFA (estructurado: debilidades/fortalezas/oportunidades/amenazas)
    analisis_dofa: Mapped[dict] = mapped_column(JSONB, default=lambda: dict(DOFA_DEFAULT))

    # Bloque FACTORES RELEVANTES (insights + indicadores economicos y financieros)
    factores_relevantes: Mapped[dict] = mapped_column(
        JSONB, default=lambda: dict(FACTORES_RELEVANTES_DEFAULT)
    )

    # Bloque CLASIFICACION PROVEEDORES (4 categorias Kraljic, listas de texto)
    clasificacion_proveedores: Mapped[dict] = mapped_column(
        JSONB, default=lambda: {k: list(v) for k, v in CLASIFICACION_PROVEEDORES_DEFAULT.items()}
    )

    # Bloque KRALJIC (cuadrante de la familia)
    kraljic: Mapped[CuadranteKraljic | None] = mapped_column(
        Enum(CuadranteKraljic, name="cuadrante_kraljic"), nullable=True
    )

    # Bloque PODER DE NEGOCIACION (Veolia / Proveedor: bajo o alto)
    poder_negociacion: Mapped[dict] = mapped_column(
        JSONB, default=lambda: dict(PODER_NEGOCIACION_DEFAULT)
    )

    # Bloque ACTORES PRINCIPALES
    actores_principales: Mapped[str] = mapped_column(Text, default="")

    # Bloque PREMISAS DE NEGOCIACION
    premisas_negociacion: Mapped[str] = mapped_column(Text, default="")

    # Bloque CLASIFICACION CLIENTE INTERNO (recurrentes / ocasionales -> spend / # OCs)
    clasificacion_cliente_interno: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {k: dict(v) for k, v in CLASIFICACION_CLIENTE_INTERNO_DEFAULT.items()},
    )

    # Bloque SUBFAMILIAS
    subfamilias: Mapped[str] = mapped_column(Text, default="")

    # Bloque ESTRATEGIA A APLICAR
    estrategia_aplicar: Mapped[str] = mapped_column(Text, default="")

    # Metadatos de control
    estado: Mapped[EstadoFicha] = mapped_column(
        Enum(EstadoFicha, name="estado_ficha"), default=EstadoFicha.BORRADOR, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    created_by_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    creador = relationship("User", back_populates="fichas_creadas", foreign_keys=[created_by_id])
    modificador = relationship("User", foreign_keys=[updated_by_id])

    revision_estrategica = relationship(
        "RevisionEstrategica", back_populates="familia", uselist=False, cascade="all, delete-orphan"
    )