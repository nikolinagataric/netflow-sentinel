# NetFlow Sentinel

NetFlow Sentinel is a Python project for processing CICIDS2017 network traffic flow data. It validates, cleans, annotates and analyzes flow records, with an optional machine learning step and a simple dashboard for viewing the results.

The main focus of the project is the data pipeline: reading raw flow data, checking it, preparing it, adding useful annotations, and exporting results in a reproducible way.

## What the Project Does

- reads CICIDS2017 CSV flow files
- validates expected columns and values
- cleans missing, infinite and duplicate values
- creates additional network-related features
- maps raw labels into simpler categories like traffic type, attack family and risk level
- exports processed data and JSON reports
- optionally trains a basic BENIGN vs ATTACK classifier
- provides a Streamlit dashboard for result overview

## Dataset

This project uses CICIDS2017 CSV flow files.

The raw dataset is not included in this repository because the files are large. To run the project locally, download the CICIDS2017 CSV files separately and place them in:

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
-> Dashboard
```

## Project Structure

```text
netflow-sentinel/
├── src/              # pipeline modules and CLI tools
├── tests/            # pytest test suite
├── dashboard/        # Streamlit dashboard
├── data/             # raw and processed data folders
├── reports/          # generated JSON reports
├── models/           # generated ML model files
├── docs/             # project notes
├── infra/            # infrastructure placeholder
├── notebooks/        # exploratory notebooks
├── requirements.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
└── README.md
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Run Tests

```powershell
pytest
```

### Inspect Dataset

Use this before running the full pipeline to check labels and row distribution:

```powershell
python -m src.inspect_dataset --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
```

### Run Pipeline

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000
```

### Run Pipeline With ML

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000 --train-model
```

### Run Dashboard

The dashboard reads generated files from `data/processed/` and `reports/`.

```powershell
streamlit run dashboard/app.py
```

### Run With Docker

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

These results are from local sample runs and can change depending on the selected file and row limit.

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

The model is intentionally simple. I used it only to show that the processed data can be used for a downstream classification task, not as a production-ready intrusion detection system.

## Annotation Logic

The annotation layer maps raw CICIDS2017 labels into simpler categories:

- `BENIGN` -> `normal` / `benign` / `low`
- `DDoS` / `DoS` -> `attack` / `denial_of_service` / `critical`
- `PortScan` -> `attack` / `reconnaissance` / `medium`
- `Patator` -> `attack` / `brute_force` / `high`
- `Web Attack` -> `attack` / `web_attack` / `high`
- `Bot` -> `attack` / `botnet` / `high`
- `Infiltration` -> `attack` / `infiltration` / `critical`
- unknown attack labels -> `attack` / `other_attack` / `high`

Flows with `medium`, `high` or `critical` risk are marked for manual review.

## AWS Deployment

The AWS deployment has been tested on a small sample file. The cloud pipeline uses S3, ECR, AWS Lambda, Step Functions and Terraform.

The AWS test used `sample_flows.csv` to keep the execution small and cheap. The local pipeline, Docker image and dashboard still work without AWS.

The detailed deployment plan is documented in:

```text
docs/aws_deployment_guide.md
```

## Future Improvements

- PCAP/PCAPNG reader
- multi-file processing
- more detailed model evaluation
- cloud orchestration example
- Terraform skeleton
- richer dashboard views

## Notes

- raw datasets and generated outputs are ignored by Git
- dataset files must be downloaded separately
- this is a portfolio/learning project focused on data processing and pipeline structure
