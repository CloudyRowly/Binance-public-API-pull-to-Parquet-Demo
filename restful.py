from binance.spot import Spot
import pandas as pd
import os
import time
from utils import *

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