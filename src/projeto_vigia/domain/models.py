from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime

class FocoQueimada(BaseModel):
    data_hora: datetime
    lat: float
    lon: float
    estado_nome: str
    municipio_nome: str
    Bioma: str
    DiaSemChuva: float | None
    RiscoFogo: float
