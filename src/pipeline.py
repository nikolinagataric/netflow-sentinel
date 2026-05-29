import argparse
from pathlib import Path

from src.annotate import annotate_flows
from src.clean import clean_flows
from src.export import create_annotation_summary, save_dataframe, save_json
from src.features import add_network_features
from src.readers.csv_flow_reader import CSVFlowReader
from src.readers.pcap_flow_reader import PCAPFlowReader
from src.train import train_binary_classifier
from src.validate import validate_schema, validate_values


def get_reader(input_path):
    """bira pravi čitač fajla na osnovu ekstenzije."""
    # ekstenzija nam govori da li čitamo CSV ili budući PCAP format
    suffix = Path(input_path).suffix.lower()

    if suffix == ".csv":
        return CSVFlowReader()
    if suffix in {".pcap", ".pcapng"}:
        return PCAPFlowReader()

    raise ValueError(f"Unsupported input format: {suffix}")


def parse_args():
    """čita argumente koje korisnik šalje iz komandne linije."""
    parser = argparse.ArgumentParser(description="Run the NetFlow Sentinel pipeline.")
    parser.add_argument("--input", required=True, help="Input flow file path.")
    parser.add_argument(
        "--output",
        default="data/processed/annotated_flows.parquet",
        help="Output file path (.csv or .parquet).",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional maximum number of rows to process.",
    )
    parser.add_argument(
        "--train-model",
        action="store_true",
        help="Train a simple binary classifier after annotation.",
    )
    return parser.parse_args()


def run_pipeline(
    input_path,
    output_path,
    max_rows=None,
    train_model=False,
    reports_dir="reports",
    model_output_path="models/random_forest_model.joblib",
):
    """pokreće cijeli pipeline od ulaznog fajla do anotiranog izlaza."""
    print("Selecting input reader...")
    reader = get_reader(input_path)

    # prvo učitavamo sirove flow podatke
    print(f"Reading flows from {input_path}...")
    df = reader.read(input_path)

    if max_rows is not None:
        # ovo je korisno kada želimo brzo testirati samo dio fajla
        print(f"Limiting input to first {max_rows} rows...")
        df = df.head(max_rows)

    # schema validacija provjerava da li imamo sve potrebne kolone
    print("Validating schema...")
    schema_report = validate_schema(df)
    save_json(schema_report, f"{reports_dir}/schema_report.json")
    if not schema_report["is_valid"]:
        raise ValueError(
            "Invalid schema. Missing columns: "
            + ", ".join(schema_report["missing_columns"])
        )

    # value validacija ne zaustavlja pipeline, nego pravi izvještaj o problemima
    print("Validating values...")
    value_report = validate_values(df)
    save_json(value_report, f"{reports_dir}/value_report.json")

    # nakon validacije redom čistimo, dodajemo feature-e i anotiramo podatke
    print("Cleaning flows...")
    df = clean_flows(df)

    print("Adding network features...")
    df = add_network_features(df)

    print("Annotating flows...")
    df = annotate_flows(df)

    if train_model:
        # Ovaj ML korak je opcioni dodatak nakon pripreme podataka
        print("Training binary classifier...")
        model_metrics = train_binary_classifier(df, model_output_path)
        save_json(model_metrics, f"{reports_dir}/model_metrics.json")

    print(f"Saving annotated flows to {output_path}...")
    save_dataframe(df, output_path)

    # na kraju snimamo kratak izvještaj koji se može brzo pregledati
    print("Creating annotation summary...")
    annotation_summary = create_annotation_summary(df)
    save_json(annotation_summary, f"{reports_dir}/annotation_summary.json")

    print("Pipeline completed successfully.")
    return df


def main():
    """ulazna tačka kada se modul pokrene preko python -m."""
    args = parse_args()
    run_pipeline(args.input, args.output, args.max_rows, args.train_model)


if __name__ == "__main__":
    main()
