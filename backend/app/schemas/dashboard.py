from pydantic import BaseModel

from app.schemas.familia import FamiliaListItem


class ConteoPorCategoria(BaseModel):
    categoria: str
    total: int


class DashboardResponse(BaseModel):
    total_fichas: int
    fichas_activas: int
    fichas_borrador: int
    fichas_archivadas: int
    ultimas_fichas: list[FamiliaListItem]
    distribucion_kraljic: list[ConteoPorCategoria]
    distribucion_estado: list[ConteoPorCategoria]
