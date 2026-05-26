from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


EXCLUDED_FEATURE_COLUMNS = {
    "label",
    "attack_family",
    "risk_level",
    "traffic_type",
    "needs_manual_review",
    "is_attack",
}


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """vraća numeričke kolone koje model smije koristiti."""
    # Ovdje izdvajamo kolone koje model smije koristiti
    numeric_columns = df.select_dtypes(include="number").columns
    return [
        column
        for column in numeric_columns
        if column not in EXCLUDED_FEATURE_COLUMNS
    ]


def train_binary_classifier(
    df: pd.DataFrame,
    model_output_path: str = "models/random_forest_model.joblib",
) -> dict:
    """trenira jednostavan binary classifier za normalan i napad saobraćaj."""
    if "is_attack" not in df.columns:
        raise ValueError("DataFrame mora imati is_attack kolonu za treniranje.")

    feature_columns = get_feature_columns(df)
    if not feature_columns:
        raise ValueError("Nema numeričkih feature kolona za treniranje modela.")

    # Target je is_attack: 0 za normalan saobraćaj, 1 za napad
    X = df[feature_columns]
    y = df["is_attack"].astype(int)

    stratify = y if y.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    model_path = Path(model_output_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Model čuvamo posebno jer ne treba da bude dio Git repozitorijuma
    joblib.dump(model, model_path)

    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "feature_columns": feature_columns,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }
