import pandas as pd

from src.schema import NUMERIC_COLUMNS, REQUIRED_COLUMNS
from src.validate import validate_schema, validate_values


def make_valid_dataframe():
    # pravimo minimalan DataFrame koji ima sve obavezne kolone
    data = {column: [1] for column in NUMERIC_COLUMNS}
    data["label"] = ["BENIGN"]
    return pd.DataFrame(data, columns=REQUIRED_COLUMNS)


def test_validate_schema_is_valid_when_all_required_columns_exist():
    df = make_valid_dataframe()

    report = validate_schema(df)

    assert report["is_valid"] is True
    assert report["missing_columns"] == []


def test_validate_schema_is_invalid_when_required_column_is_missing():
    df = make_valid_dataframe().drop(columns=["label"])

    report = validate_schema(df)

    assert report["is_valid"] is False
    assert "label" in report["missing_columns"]


def test_validate_values_detects_invalid_destination_port():
    df = make_valid_dataframe()
    df.loc[0, "destination_port"] = 70000

    report = validate_values(df)

    assert report["invalid_ports"] == 1


def test_validate_values_detects_negative_numeric_values():
    df = make_valid_dataframe()
    df.loc[0, "flow_duration"] = -10
    df.loc[0, "total_fwd_packets"] = -1

    report = validate_values(df)

    assert report["negative_values"]["flow_duration"] == 1
    assert report["negative_values"]["total_fwd_packets"] == 1
