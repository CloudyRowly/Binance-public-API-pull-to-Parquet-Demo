from binance.spot import Spot
from enum import Enum
import pandas as pd
import os
import time

class Parameters(Enum):
    intervals = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    
    # Pairs
    LTCUSDT = "LTCUSDT"
    BTCUSDT = "BTCUSDT"


class Database():
    def read(file_name):
        path = os.path.join("data", file_name)
        return pd.read_parquet(path, engine="auto")
    

    def read_selective(file_name, columns):
        """Read only selected columns from parquet file.

        Args:
            file_name (_type_): _description_
            columns (_type_): _description_

        Returns:
            pandas.Dataframe: queried columns
        """
        path = os.path.join("data", file_name)
        return pd.read_parquet(path, columns=columns, engine="auto")


class Rest():
    def __init__(self):
        self.api = Spot()

    
    def get_klines(self, symbol, interval):
        return self.api.klines(symbol, interval)
    

    def get_klines_limit(self, symbol, interval, limit):
        return self.api.klines(symbol, interval, limit=limit)


    def write(self, pair, interval, limit):
        """write to parquet file.

        Args:
            pair (str): chosen trading pair
            interval (str): trading interval
            limit (int): number of interval to pull
        """
        file_name = f"{pair}_{interval}.parquet.snappy"
        path = os.path.join("data", file_name)
        temp = self.get_klines_limit(pair, interval, limit)
        data = pd.DataFrame(temp, columns=["Open time", 
                                           "Open",
                                           "High", 
                                           "Low", 
                                           "Close", 
                                           "Volume", 
                                           "Close time", 
                                           "Quote asset volume", 
                                           "Number of trades", 
                                           "Taker buy base asset volume", 
                                           "Taker buy quote asset volume",
                                           "Ignore"])
        data.to_parquet(path, compression="snappy")
        print(f"File {file_name} has been written.")
    

def time_testing():
    s = time.time()
    main.write(Parameters.LTCUSDT.value, Parameters.intervals.value[4], 1000)
    e = time.time()
    print(f"Time taken for writing: {e - s}")

    s = time.time()
    print(Database.read("LTCUSDT_15m.parquet.snappy"))
    e = time.time()
    print(f"Time taken for reading: {e - s}")

    s = time.time()
    print(Database.read_selective("LTCUSDT_15m.parquet.snappy", ["Open time", "Open", "Close time", "Close"]))
    e = time.time()
    print(f"Time taken for selective reading: {e - s}")

    s = time.time()
    main.write(Parameters.BTCUSDT.value, Parameters.intervals.value[5], 1000)
    e = time.time()
    print(f"Time taken for writing: {e - s}")

    s = time.time()
    print(Database.read("BTCUSDT_30m.parquet.snappy"))
    e = time.time()
    print(f"Time taken for reading: {e - s}")


if __name__ == "__main__":
    main = Rest()
    time_testing()