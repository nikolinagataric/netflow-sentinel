import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")


def list_files(directory: Path, pattern: str) -> list[Path]:
    """vraća sortirane fajlove ako folder postoji."""
    if not directory.exists():
        return []
    return sorted(directory.glob(pattern))


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    """učitava processed CSV fajl."""
    return pd.read_csv(path)


def load_json(path: Path) -> dict:
    """učitava JSON report ako postoji."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as report_file:
        return json.load(report_file)


def get_summary(df: pd.DataFrame) -> dict:
    """uzima summary iz reporta ili ga računa iz CSV fajla."""
    report_summary = load_json(REPORTS_DIR / "annotation_summary.json")
    if report_summary:
        return report_summary

    traffic_counts = (
        df["traffic_type"].value_counts().to_dict()
        if "traffic_type" in df.columns
        else {}
    )
    manual_review_count = (
        int((df["needs_manual_review"].astype(bool)).sum())
        if "needs_manual_review" in df.columns
        else 0
    )

    return {
        "total_rows": int(len(df)),
        "traffic_type_counts": traffic_counts,
        "manual_review_count": manual_review_count,
    }


def show_metric_cards(summary: dict):
    """prikazuje glavne brojeve na vrhu dashboarda."""
    traffic_counts = summary.get("traffic_type_counts", {})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total rows", summary.get("total_rows", 0))
    col2.metric("Normal flows", traffic_counts.get("normal", 0))
    col3.metric("Attack flows", traffic_counts.get("attack", 0))
    col4.metric("Manual review", summary.get("manual_review_count", 0))


def show_distribution_chart(df: pd.DataFrame, column: str, title: str):
    """pravi bar chart samo ako kolona postoji."""
    if column not in df.columns:
        st.info(f"Column `{column}` was not found, skipping this chart.")
        return

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "count"]
    fig = px.bar(counts, x=column, y="count", title=title)
    st.plotly_chart(fig, use_container_width=True)


def show_top_ports(df: pd.DataFrame):
    """prikazuje najčešće destination portove."""
    if "destination_port" not in df.columns:
        st.info("Column `destination_port` was not found, skipping top ports chart.")
        return

    ports = df["destination_port"].value_counts().head(10).reset_index()
    ports.columns = ["destination_port", "count"]
    fig = px.bar(ports, x="destination_port", y="count", title="Top 10 destination ports")
    st.plotly_chart(fig, use_container_width=True)


def show_selected_report(report_files: list[Path]):
    """omogućava brz pregled JSON reporta iz reports foldera."""
    if not report_files:
        st.sidebar.info("No report files found.")
        return

    selected_report = st.sidebar.selectbox(
        "Report file",
        report_files,
        format_func=lambda path: path.name,
    )
    with st.expander(f"Selected report: {selected_report.name}"):
        st.json(load_json(selected_report))


def show_ml_metrics():
    """prikazuje ML metrike ako je report generisan."""
    st.subheader("ML metrics")
    metrics = load_json(REPORTS_DIR / "model_metrics.json")
    if not metrics:
        st.info("ML metrics report was not found.")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accuracy", metrics.get("accuracy", 0))
    col2.metric("Precision", metrics.get("precision", 0))
    col3.metric("Recall", metrics.get("recall", 0))
    col4.metric("F1 score", metrics.get("f1_score", 0))

    col5, col6 = st.columns(2)
    col5.metric("Train rows", metrics.get("train_rows", 0))
    col6.metric("Test rows", metrics.get("test_rows", 0))

    confusion_matrix = metrics.get("confusion_matrix")
    if confusion_matrix:
        fig = px.imshow(
            confusion_matrix,
            text_auto=True,
            title="Confusion matrix",
            labels={"x": "Predicted", "y": "Actual"},
        )
        st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(page_title="NetFlow Sentinel Dashboard", layout="wide")

    st.title("NetFlow Sentinel Dashboard")
    st.write(
        "Interactive overview of processed network traffic flows and generated pipeline reports."
    )

    if not PROCESSED_DIR.exists():
        st.warning("`data/processed/` folder does not exist yet.")
        return

    csv_files = list_files(PROCESSED_DIR, "*.csv")
    if not csv_files:
        st.warning("No processed CSV files found in `data/processed/`.")
        return

    selected_csv = st.sidebar.selectbox(
        "Processed CSV file",
        csv_files,
        format_func=lambda path: path.name,
    )
    report_files = list_files(REPORTS_DIR, "*.json")
    show_selected_report(report_files)

    # nakon izbora fajla učitavamo podatke za prikaz
    df = load_csv(str(selected_csv))
    summary = get_summary(df)

    show_metric_cards(summary)

    st.subheader("Charts")
    col1, col2 = st.columns(2)
    with col1:
        show_distribution_chart(df, "traffic_type", "Traffic type distribution")
        show_distribution_chart(df, "attack_family", "Attack family distribution")
    with col2:
        show_distribution_chart(df, "risk_level", "Risk level distribution")
        show_top_ports(df)

    show_ml_metrics()

    st.subheader("Data preview")
    st.dataframe(df.head(50), use_container_width=True)


if __name__ == "__main__":
    main()
