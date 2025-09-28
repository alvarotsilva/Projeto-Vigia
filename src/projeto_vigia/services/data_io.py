from __future__ import annotations
import io
import pandas as pd
from .drive_fetch import download_text_from_gdrive

def read_csv_from_gdrive(url: str) -> pd.DataFrame:
    text = download_text_from_gdrive(url)
    return pd.read_csv(io.StringIO(text))
