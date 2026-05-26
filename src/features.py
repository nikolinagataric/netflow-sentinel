import numpy as np


def add_network_features(df):
    """dodaje nove kolone koje pomažu u analizi mrežnog saobraćaja."""
    # kopiramo DataFrame da ne mijenjamo ulazne podatke
    feature_df = df.copy()

    # sabiramo pakete i bajtove iz oba smjera komunikacije
    feature_df["total_packets"] = (
        feature_df["total_fwd_packets"] + feature_df["total_backward_packets"]
    )
    feature_df["total_bytes"] = (
        feature_df["total_length_fwd_packets"] + feature_df["total_length_bwd_packets"]
    )

    # ako nema paketa, stavljamo 0 da izbjegnemo dijeljenje nulom
    feature_df["bytes_per_packet"] = np.where(
        feature_df["total_packets"] > 0,
        feature_df["total_bytes"] / feature_df["total_packets"],
        0,
    )

    # odnos forward i backward paketa može pomoći da se primijeti neobičan tok
    feature_df["fwd_bwd_packet_ratio"] = np.where(
        feature_df["total_backward_packets"] > 0,
        feature_df["total_fwd_packets"] / feature_df["total_backward_packets"],
        feature_df["total_fwd_packets"],
    )

    # well-known portovi su standardni portovi od 0 do 1023
    feature_df["is_well_known_port"] = feature_df["destination_port"].between(0, 1023)
    feature_df["is_web_traffic"] = feature_df["destination_port"].isin([80, 443])

    # ako je labela BENIGN, tretiramo flow kao normalan saobraćaj
    # sve što nije BENIGN posmatramo kao potencijalni napad
    feature_df["is_attack"] = np.where(
        feature_df["label"].astype(str).str.upper() == "BENIGN", 0, 1
    )

    return feature_df
