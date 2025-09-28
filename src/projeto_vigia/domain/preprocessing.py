from __future__ import annotations
import pandas as pd
from projeto_vigia.config import ESSENTIAL_COLS, RENAME_MAP

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Garante colunas essenciais
    if not all(c in df.columns for c in ESSENTIAL_COLS):
        missing = [c for c in ESSENTIAL_COLS if c not in df.columns]
        raise ValueError(f"CSV sem colunas essenciais: {', '.join(missing)}")

    df = df.copy()
    df.rename(columns=RENAME_MAP, inplace=True)
    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
    df["DiaSemChuva"] = pd.to_numeric(df["DiaSemChuva"], errors="coerce").replace(-999, pd.NA)
    df["RiscoFogo"] = pd.to_numeric(df["RiscoFogo"], errors="coerce")
    df.dropna(subset=["lat", "lon", "data_hora", "RiscoFogo"], inplace=True)
    return df
