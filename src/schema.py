# ovo su kolone koje moraju postojati nakon učitavanja i mapiranja CSV fajla
REQUIRED_COLUMNS = [
    "destination_port",
    "flow_duration",
    "total_fwd_packets",
    "total_backward_packets",
    "total_length_fwd_packets",
    "total_length_bwd_packets",
    "flow_bytes_per_second",
    "flow_packets_per_second",
    "syn_flag_count",
    "ack_flag_count",
    "rst_flag_count",
    "fin_flag_count",
    "label",
]


# protocol nije uvijek prisutan u CICIDS2017 CSV fajlovima, pa ga čuvamo kao opcioni
OPTIONAL_COLUMNS = [
    "protocol",
]


# ove kolone treba da budu brojevi da bi validacija i feature-i radili ispravno
NUMERIC_COLUMNS = [
    "destination_port",
    "flow_duration",
    "total_fwd_packets",
    "total_backward_packets",
    "total_length_fwd_packets",
    "total_length_bwd_packets",
    "flow_bytes_per_second",
    "flow_packets_per_second",
    "syn_flag_count",
    "ack_flag_count",
    "rst_flag_count",
    "fin_flag_count",
    "protocol",
]
