from enum import Enum
import pandas as pd
import os

class Parameters(Enum):
    intervals = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    
    # Pairs
    LTCUSDT = "LTCUSDT"
    BTCUSDT = "BTCUSDT"


class Database():
    def read(file_name):
        path = os.path.join("data", file_name)
        return pd.read_parquet(path, engine="auto")
    

    def read_selective(file_name, columns=None, filters=None):
        """Read only selected columns from parquet file.

        Args:
            file_name (str): file path
            columns ([str]): columns to be queried
            filters ([str]): row filters condition in the format
                             [("column_name", "==", value)]
                             "==" can be replaced by any other comparisons
                             ["<" , ">", "<=", ">=", "!="]

        Returns:
            pandas.Dataframe: queried columns
        """
        path = os.path.join("data", file_name)
        return pd.read_parquet(path, engine="auto", columns=columns, filters=filters)