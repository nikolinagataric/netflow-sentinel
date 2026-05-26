import pandas as pd

from src.readers.base_reader import BaseFlowReader


class PCAPFlowReader(BaseFlowReader):
    """
    planirano proširenje za buduće parsiranje PCAP/PCAPNG fajlova u isti
    standardni flow schema koji koristi ostatak pipeline-a.
    """

    def read(self, path: str) -> pd.DataFrame:
        # PCAP čitanje još nije spremno, zato ovdje jasno zaustavljamo pipeline
        raise NotImplementedError(
            "PCAP/PCAPNG parsing is not implemented yet. Use CSV input for now."
        )
