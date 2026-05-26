import pandas as pd

from src.train import get_feature_columns, train_binary_classifier


def make_training_dataframe():
    # mali skup podataka koji ne zavisi od pravog CICIDS2017 fajla
    return pd.DataFrame(
        {
            "flow_duration": [10, 20, 30, 40, 50, 60],
            "total_packets": [2, 4, 6, 8, 10, 12],
            "bytes_per_packet": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "label": ["BENIGN", "BENIGN", "DDoS", "DDoS", "PortScan", "BENIGN"],
            "attack_family": [
                "benign",
                "benign",
                "denial_of_service",
                "denial_of_service",
                "reconnaissance",
                "benign",
            ],
            "risk_level": ["low", "low", "critical", "critical", "medium", "low"],
            "traffic_type": ["normal", "normal", "attack", "attack", "attack", "normal"],
            "needs_manual_review": [False, False, True, True, True, False],
            "is_attack": [0, 0, 1, 1, 1, 0],
        }
    )


def test_get_feature_columns_excludes_target_and_annotation_columns():
    df = make_training_dataframe()

    feature_columns = get_feature_columns(df)

    assert "is_attack" not in feature_columns
    assert "label" not in feature_columns
    assert "attack_family" not in feature_columns
    assert "risk_level" not in feature_columns
    assert "traffic_type" not in feature_columns
    assert "needs_manual_review" not in feature_columns


def test_get_feature_columns_returns_numeric_feature_columns():
    df = make_training_dataframe()

    feature_columns = get_feature_columns(df)

    assert "flow_duration" in feature_columns
    assert "total_packets" in feature_columns
    assert "bytes_per_packet" in feature_columns


def test_train_binary_classifier_returns_metrics(tmp_path):
    df = make_training_dataframe()
    model_path = tmp_path / "random_forest_model.joblib"

    metrics = train_binary_classifier(df, str(model_path))

    expected_keys = {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "confusion_matrix",
        "feature_columns",
        "train_rows",
        "test_rows",
    }
    assert expected_keys.issubset(metrics.keys())
    assert model_path.exists()
