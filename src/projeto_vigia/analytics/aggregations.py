from __future__ import annotations
import pandas as pd

def by_day(df: pd.DataFrame) -> pd.DataFrame:
    dff = df.copy()
    dff["data"] = dff["data_hora"].dt.date
    return dff.groupby("data").size().reset_index(name="contagem")

def by_biome(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["Bioma"]
        .value_counts()
        .rename_axis("Bioma")
        .reset_index(name="Número de Focos")
    )

def top_municipios(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df["municipio_nome"]
        .value_counts()
        .nlargest(n)
        .rename_axis("Município")
        .reset_index(name="Número de Focos")
    )

def series_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """
    dimension ∈ {"estado_nome","Bioma"}
    Agrega focos por dia e dimensão.
    """
    dff = df.copy()
    dff["data"] = dff["data_hora"].dt.date
    out = dff.groupby(["data", dimension]).size().reset_index(name="contagem")
    return out

def compute_critical_regions(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Define 'regiões críticas' por agregação em Município + Estado + Bioma
    com métricas: focos, risco médio, FRP médio/máx, precipitação média, dias sem chuva médios.
    """
    grp = (df.groupby(["estado_nome", "municipio_nome", "Bioma"])
             .agg(
                 focos=("RiscoFogo","size"),
                 risco_medio=("RiscoFogo","mean"),
                 frp_medio=("FRP","mean"),
                 frp_max=("FRP","max"),
                 precip_media=("Precipitacao","mean"),
                 dias_sem_chuva_med=("DiaSemChuva","mean"),
                 lat=("lat","mean"),
                 lon=("lon","mean"),
             )
             .reset_index())
    # Score simples: combina quantidade de focos + risco médio + FRP médio
    grp["score"] = grp["focos"]*0.6 + grp["risco_medio"]*100*0.25 + grp["frp_medio"]*0.15
    return grp.sort_values(["score","focos","frp_medio"], ascending=False).head(top_n)
