import numpy as np
import pandas as pd

from src.clean import clean_flows


def make_flow_dataframe(rows):
    # osnovne kolone koje clean_flows koristi u testovima
    return pd.DataFrame(rows)


def test_clean_flows_removes_duplicates():
    df = make_flow_dataframe(
        [
            {"destination_port": 80, "flow_duration": 10, "label": "BENIGN"},
            {"destination_port": 80, "flow_duration": 10, "label": "BENIGN"},
        ]
    )

    cleaned = clean_flows(df)

    assert len(cleaned) == 1


def test_clean_flows_replaces_inf_and_fills_numeric_nan_values():
    df = make_flow_dataframe(
        [
            {"destination_port": 80, "flow_duration": np.inf, "label": "BENIGN"},
            {"destination_port": 443, "flow_duration": 20, "label": "BENIGN"},
            {"destination_port": 53, "flow_duration": np.nan, "label": "BENIGN"},
        ]
    )

    cleaned = clean_flows(df)

    assert cleaned["flow_duration"].isna().sum() == 0
    assert np.isinf(cleaned["flow_duration"]).sum() == 0
    assert cleaned["flow_duration"].tolist() == [20.0, 20.0, 20.0]


def test_clean_flows_removes_rows_with_empty_or_missing_label():
    df = make_flow_dataframe(
        [
            {"destination_port": 80, "flow_duration": 10, "label": "BENIGN"},
            {"destination_port": 443, "flow_duration": 20, "label": ""},
            {"destination_port": 53, "flow_duration": 30, "label": np.nan},
        ]
    )

    cleaned = clean_flows(df)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["label"] == "BENIGN"
