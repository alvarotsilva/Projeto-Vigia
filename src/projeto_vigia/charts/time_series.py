import altair as alt
import pandas as pd

def time_chart_overall(focos_por_dia: pd.DataFrame) -> alt.Chart:
    return (alt.Chart(focos_por_dia)
            .mark_line(point=True)
            .encode(
                x=alt.X("data:T", title="Data"),
                y=alt.Y("contagem:Q", title="Focos por dia"),
                tooltip=["data:T","contagem:Q"]
            )
            .properties(title="Evolução diária (geral)")
            .interactive())

def time_chart_by_dimension(df_series: pd.DataFrame, dimension: str) -> alt.Chart:
    # df_series: colunas: data, dimension, contagem
    return (alt.Chart(df_series)
            .mark_line(point=True)
            .encode(
                x=alt.X("data:T", title="Data"),
                y=alt.Y("contagem:Q", title="Focos por dia"),
                color=alt.Color(f"{dimension}:N", title=dimension),
                tooltip=["data:T","contagem:Q", alt.Tooltip(f"{dimension}:N", title=dimension)]
            )
            .properties(title=f"Evolução diária por {dimension}")
            .interactive())
