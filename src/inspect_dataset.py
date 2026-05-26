import argparse

import pandas as pd


def parse_args():
    """čita argumente za mali alat za pregled dataset-a."""
    parser = argparse.ArgumentParser(description="Inspect CICIDS2017 CSV labels.")
    parser.add_argument("--input", required=True, help="Putanja do CSV fajla.")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Opcionalan broj redova za učitavanje.",
    )
    return parser.parse_args()


def inspect_dataset(input_path, max_rows=None):
    """učitava CSV i prikazuje osnovne informacije o labelama."""
    # ako je max_rows postavljen, učitavamo samo početak fajla
    df = pd.read_csv(input_path, nrows=max_rows)

    # CICIDS2017 često ima razmake u nazivima kolona
    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        raise ValueError("CSV fajl nema Label kolonu nakon uklanjanja razmaka.")

    labels = df["Label"].astype(str).str.strip()
    label_counts = labels.value_counts(dropna=False)
    label_percentages = (label_counts / len(labels) * 100).round(4)

    # tražimo prvi red koji nije BENIGN da znamo gdje počinju napadi
    non_benign_mask = labels.str.upper() != "BENIGN"
    first_attack_index = None
    if non_benign_mask.any():
        first_attack_index = int(non_benign_mask.idxmax())

    print(f"Input file: {input_path}")
    print(f"Total rows loaded: {len(df)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nLabel counts:")
    for label, count in label_counts.items():
        print(f"- {label}: {int(count)}")

    print("\nLabel percentages:")
    for label, percentage in label_percentages.items():
        print(f"- {label}: {percentage}%")

    print("\nFirst 5 label values:")
    print(labels.head(5).to_string(index=True))

    print("\nLast 5 label values:")
    print(labels.tail(5).to_string(index=True))

    print("\nFirst non-BENIGN index:")
    if first_attack_index is None:
        print("No non-BENIGN label found in loaded rows.")
    else:
        print(first_attack_index)


def main():
    """ulazna tačka za pokretanje preko python -m."""
    args = parse_args()
    inspect_dataset(args.input, args.max_rows)


if __name__ == "__main__":
    main()
