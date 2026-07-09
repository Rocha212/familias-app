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


# Estructura por defecto de los bloques JSON, usada al crear una ficha nueva
STATUS_DEFAULT = {
    "spend_2025": 0,
    "num_proveedores": 0,
    "spend_under_control": 0,
    "num_proveedores_suc": 0,
}

CLASIFICACION_PROVEEDORES_DEFAULT = {
    "estrategicos": [],
    "clave": [],
    "tacticos": [],
}

CLASIFICACION_CLIENTE_INTERNO_DEFAULT = {
    "estrategicos": {"spend": 0, "ocs": 0},
    "clave": {"spend": 0, "ocs": 0},
    "tacticos": {"spend": 0, "ocs": 0},
}


class Familia(Base):
    """Ficha de estandarizacion de una familia de abastecimiento (Fase 1)."""

    __tablename__ = "familias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Encabezado
    linea_abastecimiento: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    descripcion_familia: Mapped[str] = mapped_column(Text, default="")
    lider: Mapped[str] = mapped_column(String(150), default="")

    # Bloque STATUS
    status: Mapped[dict] = mapped_column(JSONB, default=lambda: dict(STATUS_DEFAULT))

    # Bloque ANALISIS (DOFA)
    analisis_dofa: Mapped[str] = mapped_column(Text, default="")

    # Bloque FACTORES RELEVANTES / Insights
    factores_relevantes: Mapped[str] = mapped_column(Text, default="")

    # Bloque CLASIFICACION PROVEEDORES (listas por categoria)
    clasificacion_proveedores: Mapped[dict] = mapped_column(
        JSONB, default=lambda: dict(CLASIFICACION_PROVEEDORES_DEFAULT)
    )

    # Bloque KRALJIC
    kraljic: Mapped[CuadranteKraljic | None] = mapped_column(
        Enum(CuadranteKraljic, name="cuadrante_kraljic"), nullable=True
    )

    # Bloque ACTORES PRINCIPALES
    actores_principales: Mapped[str] = mapped_column(Text, default="")

    # Bloque PREMISAS DE NEGOCIACION
    premisas_negociacion: Mapped[str] = mapped_column(Text, default="")

    # Bloque CLASIFICACION CLIENTE INTERNO (spend / # OCs por categoria)
    clasificacion_cliente_interno: Mapped[dict] = mapped_column(
        JSONB, default=lambda: dict(CLASIFICACION_CLIENTE_INTERNO_DEFAULT)
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
