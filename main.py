from binance_api import *
from enum import Enum
import pandas as pd
import os

class Parameters(Enum):
    intervals = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    
    # Pairs
    LTCUSDT = "LTCUSDT"
    BTCUSDT = "BTCUSDT"


class Main():
    def __init__(self):
        self.api = BinanceAPI()


    def write(self, pair, interval, limit):
        file_name = f"{pair}_{interval}.parquet.snappy"
        path = os.path.join("data", file_name)
        temp = self.api.get_klines_limit(pair, interval, limit)
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


    def read(self, file_name):
        path = os.path.join("data", file_name)
        return pd.read_parquet(path, engine="pyarrow")


if __name__ == "__main__":
    main = Main()
    
    main.write(Parameters.LTCUSDT.value, Parameters.intervals.value[4], 1000)
    print(main.read("LTCUSDT_15m.parquet.snappy"))

    main.write(Parameters.BTCUSDT.value, Parameters.intervals.value[5], 1000)
    print(main.read("BTCUSDT_30m.parquet.snappy"))