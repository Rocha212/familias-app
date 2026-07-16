from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

# ---------------------------------------------------------------------------
# Estructuras por defecto de los bloques JSON
# ---------------------------------------------------------------------------

# Serie de 3 anios, reutilizada tanto en roadmap como en beneficios_esperados
SERIE_3_ANIOS_DEFAULT = {
    "2026": "",
    "2027": "",
    "2028": "",
}

# Bloque EJES ESTRATEGICOS (Pagina 2: "Donde queremos llegar")
EJES_ESTRATEGICOS_DEFAULT = {
    "performance_economico": "",
    "performance_operacional": "",
    "riesgo": {
        "compliance": "",
        "financiero": "",
        "operativo": "",
        "ambiental_pss": "",
    },
    "innovacion": {
        "general": "",
        "crecimiento_ingresos": "",
    },
    "ambiental_social_gobernanza": {
        "decarbonizacion": "",
        "economia_circular": "",
        "creacion_valor_territorial": "",
        "derechos_humanos_compliance": "",
    },
}

# Bloque BENEFICIOS ESPERADOS (Pagina 3: "Que resultados esperamos")
# 7 ejes, cada uno con su serie de 3 anios.
BENEFICIOS_ESPERADOS_EJES = (
    "spend_under_control",
    "performance_economico",
    "performance_operativo",
    "riesgo",
    "innovacion",
    "crecimiento_ingresos",
    "ambiental_social_gobernanza",
)
BENEFICIOS_ESPERADOS_DEFAULT = {
    eje: dict(SERIE_3_ANIOS_DEFAULT) for eje in BENEFICIOS_ESPERADOS_EJES
}


class RevisionEstrategica(Base):
    """Paginas 2 y 3 de la ficha: 'Donde queremos llegar' y 'Que resultados esperamos'.

    Relacion 1 a 1 con Familia (una ficha tiene, a lo sumo, una revision estrategica).
    Se crea bajo demanda cuando el usuario abre estas paginas por primera vez.
    """

    __tablename__ = "revisiones_estrategicas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    familia_id: Mapped[int] = mapped_column(
        ForeignKey("familias.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )

    # Pagina 2 - Donde queremos llegar
    objetivo_estrategico: Mapped[str] = mapped_column(Text, default="")
    ejes_estrategicos: Mapped[dict] = mapped_column(
        JSONB, default=lambda: dict(EJES_ESTRATEGICOS_DEFAULT)
    )
    roadmap: Mapped[dict] = mapped_column(JSONB, default=lambda: dict(SERIE_3_ANIOS_DEFAULT))

    # Pagina 3 - Que resultados esperamos
    beneficios_esperados: Mapped[dict] = mapped_column(
        JSONB, default=lambda: {k: dict(v) for k, v in BENEFICIOS_ESPERADOS_DEFAULT.items()}
    )

    # Metadatos de control (mismo patron que Familia)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    familia = relationship("Familia", back_populates="revision_estrategica")
    creador = relationship("User", foreign_keys=[created_by_id])
    modificador = relationship("User", foreign_keys=[updated_by_id])