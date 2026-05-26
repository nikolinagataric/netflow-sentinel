from abc import ABC, abstractmethod

import pandas as pd


class BaseFlowReader(ABC):
    """osnovna klasa za sve čitače flow podataka."""

    @abstractmethod
    def read(self, path: str) -> pd.DataFrame:
        """učitava podatke i vraća ih kao pandas DataFrame."""
        raise NotImplementedError
