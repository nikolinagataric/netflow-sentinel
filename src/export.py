import json
from pathlib import Path


def ensure_directory(path):
    """pravi folder ako već ne postoji."""
    Path(path).mkdir(parents=True, exist_ok=True)


def save_json(data, path):
    """snima podatke u JSON fajl."""
    output_path = Path(path)

    # prije snimanja pravimo folder za izlazni fajl
    ensure_directory(output_path.parent)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=2)


def save_dataframe(df, path):
    """snima DataFrame kao CSV ili Parquet, zavisno od ekstenzije."""
    output_path = Path(path)
    ensure_directory(output_path.parent)

    # ekstenzija određuje format u kojem čuvamo rezultat
    suffix = output_path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(output_path, index=False)
        return
    if suffix == ".parquet":
        df.to_parquet(output_path, index=False)
        return

    raise ValueError(f"Unsupported output format: {suffix}")


def create_annotation_summary(df):
    """pravi kratak pregled anotiranih flow podataka."""
    # value_counts nam daje koliko puta se pojavljuje svaka kategorija
    return {
        "total_rows": int(len(df)),
        "traffic_type_counts": _value_counts_as_ints(df, "traffic_type"),
        "risk_level_counts": _value_counts_as_ints(df, "risk_level"),
        "attack_family_counts": _value_counts_as_ints(df, "attack_family"),
        "manual_review_count": int(df["needs_manual_review"].sum()),
    }


def _value_counts_as_ints(df, column):
    """pretvara pandas brojače u obične int vrijednosti za JSON."""
    return {key: int(value) for key, value in df[column].value_counts().items()}
