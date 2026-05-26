import numpy as np
import pandas as pd

from src.schema import NUMERIC_COLUMNS


def clean_flows(df):
    """čisti flow podatke prije dodavanja novih feature-a."""
    # kopiramo DataFrame da ne mijenjamo originalne podatke
    clean_df = df.copy()

    # beskonačne vrijednosti mijenjamo u NaN jer ih pandas lakše obrađuje
    clean_df = clean_df.replace([np.inf, -np.inf], np.nan)
    clean_df = clean_df.drop_duplicates()

    # numeričke kolone pretvaramo u brojeve, a loše vrijednosti postaju NaN
    existing_numeric_columns = [
        column for column in NUMERIC_COLUMNS if column in clean_df.columns
    ]
    for column in existing_numeric_columns:
        clean_df[column] = pd.to_numeric(clean_df[column], errors="coerce")

    if "label" in clean_df.columns:
        # redovi bez labele nam ne pomažu za anotaciju
        clean_df = clean_df.dropna(subset=["label"])
        clean_df = clean_df[clean_df["label"].astype(str).str.strip() != ""]

    # prazne numeričke vrijednosti popunjavamo medianom iz iste kolone
    for column in existing_numeric_columns:
        median_value = clean_df[column].median()
        if pd.isna(median_value):
            median_value = 0
        clean_df[column] = clean_df[column].fillna(median_value)

    return clean_df
