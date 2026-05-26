def get_attack_family(label):
    """pretvara originalnu labelu u širu porodicu napada."""
    # normalizujemo tekst da poređenje bude jednostavnije
    normalized_label = str(label).strip()
    lower_label = normalized_label.lower()

    # poznate CICIDS2017 labele svodimo na manje grupa
    if lower_label == "benign":
        return "benign"
    if "portscan" in lower_label:
        return "reconnaissance"
    if "dos" in lower_label or "ddos" in lower_label:
        return "denial_of_service"
    if "patator" in lower_label:
        return "brute_force"
    if "web attack" in lower_label:
        return "web_attack"
    if "bot" in lower_label:
        return "botnet"
    if "infiltration" in lower_label:
        return "infiltration"

    return "other_attack"


def get_risk_level(attack_family):
    """dodjeljuje jednostavan nivo rizika za porodicu napada."""
    # ovdje držimo pravila za rizik na jednom mjestu
    risk_levels = {
        "benign": "low",
        "reconnaissance": "medium",
        "denial_of_service": "critical",
        "brute_force": "high",
        "web_attack": "high",
        "botnet": "high",
        "infiltration": "critical",
        "other_attack": "high",
    }
    return risk_levels.get(attack_family, "high")


def annotate_flows(df):
    """dodaje kolone koje olakšavaju čitanje i pregled rezultata."""
    # kopiramo DataFrame da original ostane nepromijenjen
    annotated_df = df.copy()

    # prvo određujemo porodicu napada, pa iz nje izvodimo rizik i tip saobraćaja
    annotated_df["attack_family"] = annotated_df["label"].apply(get_attack_family)
    annotated_df["risk_level"] = annotated_df["attack_family"].apply(get_risk_level)
    annotated_df["traffic_type"] = annotated_df["attack_family"].apply(
        lambda family: "normal" if family == "benign" else "attack"
    )

    # sve iznad low rizika šaljemo na ručni pregled
    annotated_df["needs_manual_review"] = annotated_df["risk_level"].isin(
        ["medium", "high", "critical"]
    )

    return annotated_df
