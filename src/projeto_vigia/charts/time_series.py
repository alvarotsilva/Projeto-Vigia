import altair as alt
import pandas as pd
from projeto_vigia.config import PRIMARY_COLOR

def time_chart(focos_por_dia: pd.DataFrame) -> alt.Chart:
    return (alt.Chart(focos_por_dia)
            .mark_line(point=True, color=PRIMARY_COLOR)
            .encode(x=alt.X("data:T", title="Data"),
                    y=alt.Y("contagem:Q", title="Número de Focos Diários"),
                    tooltip=["data:T", "contagem:Q"])
            .properties(title="Evolução Diária dos Focos de Queimada")
            .interactive())
