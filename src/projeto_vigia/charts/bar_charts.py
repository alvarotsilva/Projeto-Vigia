import altair as alt
import pandas as pd
from projeto_vigia.config import PRIMARY_COLOR

def bioma_chart(df_bioma: pd.DataFrame) -> alt.Chart:
    return (alt.Chart(df_bioma)
            .mark_bar()
            .encode(x=alt.X("Número de Focos:Q"),
                    y=alt.Y("Bioma:N", sort="-x"),
                    tooltip=["Bioma", "Número de Focos"],
                    color=alt.Color("Bioma:N", legend=None, scale=alt.Scale(scheme="redyellowgreen")))
            .properties(title="Focos de Queimada por Bioma"))

def municipio_chart(df_mun: pd.DataFrame) -> alt.Chart:
    return (alt.Chart(df_mun)
            .mark_bar(color=PRIMARY_COLOR)
            .encode(x=alt.X("Número de Focos:Q"),
                    y=alt.Y("Município:N", sort="-x"),
                    tooltip=["Município", "Número de Focos"])
            .properties(title="Top 10 Municípios com Mais Focos"))
