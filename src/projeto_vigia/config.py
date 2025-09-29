from __future__ import annotations

PRIMARY_COLOR = "#ff6347"  # Tomate
FILE_URL = "https://drive.google.com/uc?export=download&id=1YlThY76iiE6TwU9ZPlBfNkm8FsccjCZm"
LOGO_URL = "https://drive.google.com/uc?export=download&id=1sUYhDEuduVYtF9dBn0CcIRYiMT9qc7o4"

ESSENTIAL_COLS = [
    "DataHora", "Latitude", "Longitude", "Estado", "Municipio", "Bioma", "DiaSemChuva", "RiscoFogo"
]

RENAME_MAP = {
    "DataHora": "data_hora",
    "Latitude": "lat",
    "Longitude": "lon",
    "Estado": "estado_nome",
    "Municipio": "municipio_nome",
}
