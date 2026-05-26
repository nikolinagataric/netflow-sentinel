# NetFlow Sentinel

A modular Python data pipeline for network traffic validation, risk annotation, and downstream threat detection.

NetFlow Sentinel is a Python data pipeline for processing, validating, annotating, and analyzing network traffic flow data. It is built around CICIDS2017 CSV flow files and keeps the workflow modular, testable, and easy to run from the command line.

The project focuses on the data pipeline first: ingestion, schema checks, value checks, cleaning, feature engineering, risk annotation, export, reporting, and optional downstream machine learning readiness.

## Key Features

- CICIDS2017 CSV flow ingestion
- schema and value validation
- data cleaning for NaN, infinite values and duplicates
- network-specific feature engineering
- risk annotation workflow
- dataset inspection CLI
- optional binary ML classifier
- pytest test suite
- planned PCAP extension

## Why This Project

This project is inspired by data pipeline principles used in sensor-data processing systems. Instead of automotive sensor data, NetFlow Sentinel works with network traffic telemetry, but the core ideas are similar:

- ingestion from raw files
- validation before processing
- cleaning and normalization
- annotation for downstream analysis
- reproducible pipeline execution
- machine learning readiness after data preparation

The goal is not to present a production intrusion detection system. The goal is to show a clear, engineering-oriented workflow for turning raw telemetry data into validated, enriched, and usable outputs.

## Dataset

NetFlow Sentinel uses CICIDS2017 CSV flow files.

The raw dataset is not included in this repository because the files are large. To run the pipeline, download the CICIDS2017 CSV files separately and place them in:

```text
data/raw/
```

Tested files include:

- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`

## Pipeline Overview

```text
CSV flow file
-> Reader
-> Schema validation
-> Value validation
-> Cleaning
-> Feature engineering
-> Risk annotation
-> Export processed data and reports
-> Optional ML training
```

## Project Structure

```text
netflow-sentinel/
├── src/              # pipeline modules and CLI tools
├── tests/            # pytest test suite
├── data/             # raw and processed data folders
├── reports/          # generated JSON reports
├── models/           # generated ML model files
├── docs/             # project notes
├── infra/            # infrastructure placeholder
├── notebooks/        # exploratory notebooks
├── requirements.txt
├── pytest.ini
└── README.md
```

## Main Commands

Install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run tests:

```powershell
pytest
```

Inspect a dataset before running the full pipeline:

```powershell
python -m src.inspect_dataset --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
```

Run the pipeline:

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000
```

Run the pipeline with optional ML training:

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000 --train-model
```

## Docker Usage

Build image:

```powershell
docker build -t netflow-sentinel .
```

Show pipeline help:

```powershell
docker run --rm netflow-sentinel --help
```

Run pipeline with local data mounted, PowerShell version:

```powershell
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/reports:/app/reports netflow-sentinel --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000
```

Run pipeline with ML:

```powershell
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/reports:/app/reports -v ${PWD}/models:/app/models netflow-sentinel --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000 --train-model
```

## Example Results

The numbers below were generated from local sample runs and may change if a different row limit or dataset file is used.

### DDoS Example Summary

From `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` with `--max-rows 50000`:

- `total_rows`: 48207
- `traffic_type normal`: 24391
- `traffic_type attack`: 23816
- `risk low`: 24391
- `risk critical`: 23816
- `attack_family benign`: 24391
- `attack_family denial_of_service`: 23816
- `manual_review_count`: 23816

### PortScan Example Summary

From the tested PortScan sample:

- `traffic_type normal`: 45908
- `traffic_type attack`: 213
- `risk low`: 45908
- `risk medium`: 213
- `attack_family benign`: 45908
- `attack_family reconnaissance`: 213
- `manual_review_count`: 213

### ML Example

The optional ML step trains a simple `RandomForestClassifier` for binary classification:

- `0`: BENIGN / normal traffic
- `1`: ATTACK / malicious traffic

Example metrics from the limited DDoS sample:

- `accuracy`: 1.0
- `precision`: 1.0
- `recall`: 1.0
- `f1_score`: 1.0
- `train_rows`: 38565
- `test_rows`: 9642

These metrics were obtained on a limited DDoS sample and should not be interpreted as a production-grade intrusion detection result. The ML step is included to demonstrate downstream readiness of the processed data.

## Annotation Logic

The annotation layer maps raw CICIDS2017 labels into simpler operational categories:

- `BENIGN` -> `normal`, `benign`, `low`, no manual review
- `DDoS` / `DoS` -> `attack`, `denial_of_service`, `critical`, manual review
- `PortScan` -> `attack`, `reconnaissance`, `medium`, manual review
- `Patator` -> `attack`, `brute_force`, `high`, manual review
- `Web Attack` -> `attack`, `web_attack`, `high`, manual review
- `Bot` -> `attack`, `botnet`, `high`, manual review
- `Infiltration` -> `attack`, `infiltration`, `critical`, manual review
- unknown attack labels -> `attack`, `other_attack`, `high`, manual review

## Future Improvements

- PCAP/PCAPNG reader implementation, currently planned and not implemented yet
- Dockerized execution
- AWS Step Functions orchestration
- Terraform infrastructure skeleton
- more advanced model evaluation
- multi-file dataset processing

## Important Notes

- `data/raw/`, `data/processed/`, `reports/`, and `models/` are ignored by Git.
- CICIDS2017 dataset files must be downloaded separately.
- This project is educational and portfolio-oriented.
- The main focus is the data pipeline. The ML step is intentionally simple and optional.
