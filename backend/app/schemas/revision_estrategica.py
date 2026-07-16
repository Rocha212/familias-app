from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.revision_estrategica import (
    SERIE_3_ANIOS_DEFAULT,
    EJES_ESTRATEGICOS_DEFAULT,
    BENEFICIOS_ESPERADOS_DEFAULT,
)


class Serie3AniosBlock(BaseModel):
    """Valores de texto libre para los anios 2026, 2027 y 2028."""

    model_config = ConfigDict(populate_by_name=True)

    year_2026: str = Field(default="", alias="2026")
    year_2027: str = Field(default="", alias="2027")
    year_2028: str = Field(default="", alias="2028")


class RiesgoBlock(BaseModel):
    compliance: str = ""
    financiero: str = ""
    operativo: str = ""
    ambiental_pss: str = ""


class InnovacionBlock(BaseModel):
    general: str = ""
    crecimiento_ingresos: str = ""


class AmbientalSocialGobernanzaBlock(BaseModel):
    decarbonizacion: str = ""
    economia_circular: str = ""
    creacion_valor_territorial: str = ""
    derechos_humanos_compliance: str = ""


class EjesEstrategicosBlock(BaseModel):
    performance_economico: str = ""
    performance_operacional: str = ""
    riesgo: RiesgoBlock = Field(default_factory=RiesgoBlock)
    innovacion: InnovacionBlock = Field(default_factory=InnovacionBlock)
    ambiental_social_gobernanza: AmbientalSocialGobernanzaBlock = Field(
        default_factory=AmbientalSocialGobernanzaBlock
    )


class BeneficiosEsperadosBlock(BaseModel):
    spend_under_control: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    performance_economico: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    performance_operativo: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    riesgo: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    innovacion: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    crecimiento_ingresos: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    ambiental_social_gobernanza: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)


class RevisionEstrategicaBase(BaseModel):
    objetivo_estrategico: str = ""
    ejes_estrategicos: EjesEstrategicosBlock = Field(default_factory=EjesEstrategicosBlock)
    roadmap: Serie3AniosBlock = Field(default_factory=Serie3AniosBlock)
    beneficios_esperados: BeneficiosEsperadosBlock = Field(default_factory=BeneficiosEsperadosBlock)


class RevisionEstrategicaCreate(RevisionEstrategicaBase):
    pass


class RevisionEstrategicaUpdate(BaseModel):
    objetivo_estrategico: str | None = None
    ejes_estrategicos: EjesEstrategicosBlock | None = None
    roadmap: Serie3AniosBlock | None = None
    beneficios_esperados: BeneficiosEsperadosBlock | None = None


class RevisionEstrategicaOut(RevisionEstrategicaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    familia_id: int
    created_at: datetime
    updated_at: datetime
    created_by_id: int
    creador_nombre: str = ""
    modificador_nombre: str | None = None