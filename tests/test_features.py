import pandas as pd

from src.features import add_network_features


def make_feature_dataframe():
    # mali primjer dovoljan za računanje novih feature kolona
    return pd.DataFrame(
        [
            {
                "destination_port": 80,
                "total_fwd_packets": 10,
                "total_backward_packets": 5,
                "total_length_fwd_packets": 500,
                "total_length_bwd_packets": 250,
                "label": "BENIGN",
            },
            {
                "destination_port": 4444,
                "total_fwd_packets": 4,
                "total_backward_packets": 2,
                "total_length_fwd_packets": 400,
                "total_length_bwd_packets": 200,
                "label": "DoS Hulk",
            },
        ]
    )


def test_add_network_features_adds_expected_columns():
    df = make_feature_dataframe()

    result = add_network_features(df)

    expected_columns = {
        "total_packets",
        "total_bytes",
        "bytes_per_packet",
        "fwd_bwd_packet_ratio",
        "is_well_known_port",
        "is_web_traffic",
        "is_attack",
    }
    assert expected_columns.issubset(result.columns)


def test_add_network_features_marks_benign_as_not_attack():
    df = make_feature_dataframe()

    result = add_network_features(df)

    assert result.loc[0, "is_attack"] == 0


def test_add_network_features_marks_non_benign_as_attack():
    df = make_feature_dataframe()

    result = add_network_features(df)

    assert result.loc[1, "is_attack"] == 1
