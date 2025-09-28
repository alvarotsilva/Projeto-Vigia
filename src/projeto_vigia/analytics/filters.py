from __future__ import annotations
import pandas as pd

def filter_by_state_and_date(df: pd.DataFrame, estado: str | None,
                             start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    dff = df if not estado or estado == "Todos" else df[df["estado_nome"] == estado]
    mask = (dff["data_hora"] >= start_date) & (dff["data_hora"] < end_date + pd.Timedelta(days=1))
    return dff.loc[mask].copy()
