import pandas as pd

from src.schema import REQUIRED_COLUMNS
from src.readers.base_reader import BaseFlowReader


# ovdje prevodimo CICIDS2017 nazive kolona u jednostavniji snake_case format
CICIDS2017_COLUMN_MAP = {
    "Destination Port": "destination_port",
    "Flow Duration": "flow_duration",
    "Total Fwd Packets": "total_fwd_packets",
    "Total Backward Packets": "total_backward_packets",
    "Total Length of Fwd Packets": "total_length_fwd_packets",
    "Total Length of Bwd Packets": "total_length_bwd_packets",
    "Flow Bytes/s": "flow_bytes_per_second",
    "Flow Packets/s": "flow_packets_per_second",
    "SYN Flag Count": "syn_flag_count",
    "ACK Flag Count": "ack_flag_count",
    "RST Flag Count": "rst_flag_count",
    "FIN Flag Count": "fin_flag_count",
    "Protocol": "protocol",
    "Label": "label",
}


class CSVFlowReader(BaseFlowReader):
    """čita CICIDS2017 CSV fajlove i vraća standardizovane kolone."""

    def read(self, path: str) -> pd.DataFrame:
        # ovdje učitavamo CSV fajl u pandas tabelu
        df = pd.read_csv(path)

        # uklanjamo razmake iz naziva kolona jer ih CICIDS2017 često ima
        df.columns = df.columns.str.strip()
        df = df.rename(columns=CICIDS2017_COLUMN_MAP)

        # vraćamo samo kolone koje naš pipeline zna da obradi
        available_columns = [column for column in REQUIRED_COLUMNS if column in df.columns]
        return df[available_columns]
