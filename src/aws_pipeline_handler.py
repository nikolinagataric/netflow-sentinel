from pathlib import Path

import boto3

from src.pipeline import run_pipeline


WORK_DIR = Path("/tmp/netflow-sentinel")


def _require_event_fields(event: dict, required_fields: list[str]):
    """provjeravamo da Lambda event ima osnovne podatke."""
    missing_fields = [field for field in required_fields if not event.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required event fields: {', '.join(missing_fields)}")


def _upload_file(s3_client, bucket: str, local_path: Path, s3_key: str) -> dict:
    """uploadujemo jedan lokalni fajl na S3."""
    s3_client.upload_file(str(local_path), bucket, s3_key)
    return {"bucket": bucket, "key": s3_key}


def _upload_folder(s3_client, bucket: str, folder: Path, output_prefix: str) -> list[dict]:
    """uploadujemo sve fajlove iz foldera ako postoje."""
    uploaded_files = []
    if not folder.exists():
        return uploaded_files

    for local_path in folder.rglob("*"):
        if local_path.is_file():
            relative_path = local_path.relative_to(folder).as_posix()
            s3_key = f"{output_prefix.rstrip('/')}/{relative_path}"
            uploaded_files.append(_upload_file(s3_client, bucket, local_path, s3_key))

    return uploaded_files


def handler(event, context):
    """AWS Lambda ulazna tačka za pokretanje NetFlow Sentinel pipeline-a."""
    _require_event_fields(
        event,
        ["input_bucket", "input_key", "output_bucket", "output_prefix"],
    )

    input_bucket = event["input_bucket"]
    input_key = event["input_key"]
    output_bucket = event["output_bucket"]
    output_prefix = event["output_prefix"].rstrip("/")
    max_rows = event.get("max_rows")
    train_model = bool(event.get("train_model", False))

    s3_client = boto3.client("s3")

    input_dir = WORK_DIR / "input"
    processed_dir = WORK_DIR / "processed"
    reports_dir = WORK_DIR / "reports"
    models_dir = WORK_DIR / "models"

    for folder in [input_dir, processed_dir, reports_dir, models_dir]:
        folder.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / Path(input_key).name
    output_path = processed_dir / f"{input_path.stem}_annotated.csv"
    model_path = models_dir / "random_forest_model.joblib"

    # prvo skidamo CSV iz S3 u lokalni /tmp folder
    s3_client.download_file(input_bucket, input_key, str(input_path))

    run_pipeline(
        str(input_path),
        str(output_path),
        max_rows=max_rows,
        train_model=train_model,
        reports_dir=str(reports_dir),
        model_output_path=str(model_path),
    )

    uploaded_files = []
    uploaded_files.append(
        _upload_file(
            s3_client,
            output_bucket,
            output_path,
            f"{output_prefix}/processed/{output_path.name}",
        )
    )
    uploaded_files.extend(
        _upload_folder(s3_client, output_bucket, reports_dir, f"{output_prefix}/reports")
    )

    if model_path.exists():
        uploaded_files.append(
            _upload_file(
                s3_client,
                output_bucket,
                model_path,
                f"{output_prefix}/models/{model_path.name}",
            )
        )

    return {
        "status": "success",
        "input": {"bucket": input_bucket, "key": input_key},
        "uploaded_files": uploaded_files,
    }
