import pandas as pd

from src.schema import NUMERIC_COLUMNS, REQUIRED_COLUMNS


def validate_schema(df):
    """provjerava da li DataFrame ima sve obavezne kolone."""
    # ovdje provjeravamo da li fale neke obavezne kolone
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    return {
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "missing_columns": missing_columns,
        "is_valid": len(missing_columns) == 0,
    }


def validate_values(df):
    """provjerava osnovne probleme u numeričkim vrijednostima."""
    # uzimamo samo numeričke kolone koje stvarno postoje u tabeli
    existing_numeric_columns = [
        column for column in NUMERIC_COLUMNS if column in df.columns
    ]

    # pretvaramo vrijednosti u brojeve da poređenja ne puknu zbog teksta
    numeric_df = df[existing_numeric_columns].apply(pd.to_numeric, errors="coerce")

    # brojimo prazne i negativne vrijednosti po svakoj numeričkoj koloni
    missing_values = {
        column: int(numeric_df[column].isna().sum())
        for column in existing_numeric_columns
    }
    negative_values = {
        column: int((numeric_df[column] < 0).sum())
        for column in existing_numeric_columns
    }

    invalid_ports = 0
    if "destination_port" in numeric_df.columns:
        # port mora biti u opsegu od 0 do 65535
        destination_port = numeric_df["destination_port"]
        invalid_ports = int(
            ((destination_port < 0) | (destination_port > 65535)).sum()
        )

    return {
        "missing_values": missing_values,
        "negative_values": negative_values,
        "invalid_ports": invalid_ports,
    }
