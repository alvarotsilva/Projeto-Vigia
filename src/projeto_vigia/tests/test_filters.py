import pandas as pd
from src.projeto_vigia.analytics.filters import filter_by_state_and_date

def test_filter_by_state_and_date():
    df = pd.DataFrame({
        "estado_nome": ["PE","PE","BA"],
        "data_hora": pd.to_datetime(["2024-01-01","2024-01-03","2024-01-02"])
    })
    out = filter_by_state_and_date(df, "PE", pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02"))
    assert len(out) == 1
