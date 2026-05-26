import pandas as pd

from src.export import create_annotation_summary


def test_create_annotation_summary_counts_manual_review_rows():
    # dva rizična reda treba da uđu u manual_review_count
    df = pd.DataFrame(
        {
            "traffic_type": ["normal", "attack", "attack"],
            "risk_level": ["low", "critical", "high"],
            "attack_family": ["benign", "denial_of_service", "other_attack"],
            "needs_manual_review": [False, True, True],
        }
    )

    summary = create_annotation_summary(df)

    assert summary["manual_review_count"] == 2
    assert summary["risk_level_counts"]["critical"] == 1
