from __future__ import annotations
import pandas as pd

def by_day(df: pd.DataFrame) -> pd.DataFrame:
    dff = df.copy()
    dff["data"] = dff["data_hora"].dt.date
    return dff.groupby("data").size().reset_index(name="contagem")

def by_biome(df: pd.DataFrame) -> pd.DataFrame:
    # Series -> DataFrame com colunas ['Bioma', 'Número de Focos']
    return (
        df["Bioma"]
        .value_counts()
        .rename_axis("Bioma")
        .reset_index(name="Número de Focos")
    )
def top_municipios(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    # Series -> DataFrame com colunas ['Município', 'Número de Focos']
    return (
        df["municipio_nome"]
        .value_counts()
        .nlargest(n)
        .rename_axis("Município")
        .reset_index(name="Número de Focos")
    )