import pandas as pd

from src.annotate import annotate_flows, get_attack_family, get_risk_level


def test_benign_gets_benign_family_and_low_risk():
    family = get_attack_family("BENIGN")

    assert family == "benign"
    assert get_risk_level(family) == "low"


def test_portscan_gets_reconnaissance_family_and_medium_risk():
    family = get_attack_family("PortScan")

    assert family == "reconnaissance"
    assert get_risk_level(family) == "medium"


def test_dos_and_ddos_get_denial_of_service_family_and_critical_risk():
    # DoS i DDoS tretiramo kao istu porodicu napada
    for label in ["DoS Hulk", "DDoS"]:
        family = get_attack_family(label)

        assert family == "denial_of_service"
        assert get_risk_level(family) == "critical"


def test_ftp_patator_gets_brute_force_family_and_high_risk():
    family = get_attack_family("FTP-Patator")

    assert family == "brute_force"
    assert get_risk_level(family) == "high"


def test_annotate_flows_adds_expected_columns():
    df = pd.DataFrame({"label": ["BENIGN", "DDoS", "PortScan", "Unknown Attack"]})

    result = annotate_flows(df)

    expected_columns = {
        "attack_family",
        "risk_level",
        "traffic_type",
        "needs_manual_review",
    }
    assert expected_columns.issubset(result.columns)
    assert result.loc[0, "traffic_type"] == "normal"
    assert result.loc[1, "traffic_type"] == "attack"
    assert result.loc[2, "traffic_type"] == "attack"
    assert bool(result.loc[0, "needs_manual_review"]) is False
    assert bool(result.loc[1, "needs_manual_review"]) is True
    assert bool(result.loc[2, "needs_manual_review"]) is True
    assert bool(result.loc[3, "needs_manual_review"]) is True
