# NetFlow Sentinel

NetFlow Sentinel is a Python project for processing and analyzing network traffic flow data from the CICIDS2017 dataset.

I built it as a small data pipeline project: it reads raw CSV flow files, checks the data, cleans it, adds a few useful network-related features, annotates traffic by risk, and exports processed results and reports.

The project also includes a simple ML step, a Streamlit dashboard, Docker support, and an AWS deployment setup.

## Why I Made This

I wanted to build a project that is more than just a notebook or a single script.

The main idea was to practice how a real data pipeline is structured:

```text
raw data
→ validation
→ cleaning
→ feature engineering
→ annotation
→ reports
→ optional model training
```

I chose network traffic data because I already have some background in computer networks, so concepts like ports, packets, TCP/IP traffic and attacks were easier for me to understand and explain.

## Dataset

The project uses CICIDS2017 CSV flow files.

The dataset is not included in the repository because the files are large. To run the project locally, the CSV files should be placed in:

```text
data/raw/
```

The main files I tested were:

```text
Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
```

I also use a small `sample_flows.csv` file for quick local, Docker and AWS tests.

## What the Pipeline Does

The pipeline currently supports CICIDS2017 CSV flow files.

Main steps:

```text
CSV input
→ column normalization
→ schema validation
→ value validation
→ data cleaning
→ feature engineering
→ risk annotation
→ processed CSV + JSON reports
```

The annotation step maps raw dataset labels into simpler categories:

```text
BENIGN   → normal traffic, low risk
DDoS/DoS → denial_of_service, critical risk
PortScan → reconnaissance, medium risk
Patator  → brute_force, high risk
```

Rows with medium, high or critical risk are marked for manual review.

## Project Structure

```text
netflow-sentinel/
├── src/                  # pipeline code
├── tests/                # pytest tests
├── dashboard/            # Streamlit dashboard
├── data/                 # local data folders
├── reports/              # generated reports
├── models/               # generated ML models
├── docs/                 # AWS deployment notes
├── infra/terraform/      # Terraform AWS setup
├── Dockerfile
├── Dockerfile.lambda
├── requirements.txt
└── README.md
```

Generated files, raw datasets and model outputs are ignored by Git.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run tests:

```powershell
pytest
```

## Running the Pipeline

Before running the full pipeline, I usually inspect the dataset first:

```powershell
python -m src.inspect_dataset --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
```

Run the pipeline:

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000
```

Run the pipeline with the optional ML step:

```powershell
python -m src.pipeline --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000 --train-model
```

## Dashboard

The project includes a simple Streamlit dashboard for viewing processed results.

Run it with:

```powershell
streamlit run dashboard/app.py
```

The dashboard reads generated files from:

```text
data/processed/
reports/
```

It shows traffic type distribution, risk levels, attack families, top destination ports, a data preview and ML metrics if they exist.

## Docker

Build the Docker image:

```powershell
docker build -t netflow-sentinel .
```

Show pipeline help:

```powershell
docker run --rm netflow-sentinel --help
```

Run the pipeline with local folders mounted:

```powershell
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/reports:/app/reports netflow-sentinel --input "data/raw/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv" --output "data/processed/ddos_annotated.csv" --max-rows 50000
```

## AWS Deployment

I also prepared and tested an AWS version of the pipeline.

The cloud version uses:

```text
S3           → input and output files
ECR          → Lambda Docker image
AWS Lambda   → runs the pipeline
Step Functions → starts the workflow
Terraform    → creates the infrastructure
```

The AWS test was done on the small `sample_flows.csv` file to keep the execution simple and cheap.

The test produced outputs in S3:

```text
processed/sample_flows_annotated.csv
reports/annotation_summary.json
reports/schema_report.json
reports/value_report.json
```

More details are in:

```text
docs/aws_deployment_guide.md
```

## Example Results

These results are from local test runs and can change depending on the selected file and row limit.

### DDoS sample

From `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` with `--max-rows 50000`:

```text
total rows: 48207
normal flows: 24391
attack flows: 23816
low risk: 24391
critical risk: 23816
manual review count: 23816
```

The DDoS traffic was mapped to:

```text
attack_family = denial_of_service
risk_level = critical
traffic_type = attack
```

### PortScan sample

From the tested PortScan sample:

```text
normal flows: 45908
attack flows: 213
low risk: 45908
medium risk: 213
manual review count: 213
```

The PortScan traffic was mapped to:

```text
attack_family = reconnaissance
risk_level = medium
traffic_type = attack
```

## Machine Learning Step

The ML part is intentionally simple.

It trains a basic `RandomForestClassifier` for binary classification:

```text
0 = normal traffic
1 = attack traffic
```

Example metrics from the limited DDoS sample:

```text
accuracy: 1.0
precision: 1.0
recall: 1.0
f1_score: 1.0
train rows: 38565
test rows: 9642
```

These metrics should not be interpreted as a production-level intrusion detection result. The goal of this step is only to show that the processed data can be used for a downstream classification task.

## Future Improvements

Some things I would improve next:

```text
- add real PCAP/PCAPNG parsing
- process multiple files in one run
- improve model evaluation
- add more dashboard views
- make the AWS pipeline more configurable
- add support for larger cloud runs
```

## Notes

This is a portfolio and learning project focused on data processing, pipeline structure and working with real network traffic flow data.

Raw datasets, processed outputs, reports, models and Terraform state files are not committed to Git.
