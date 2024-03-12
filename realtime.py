from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import pandas as pd
import os
import time
import json
from restful import Database

class Realtime():
    def __init__(self):
        self.ws = SpotWebsocketStreamClient(on_message=self.message_handler,
                                            is_combined=True,
                                            timeout=2)
        
        # Subscibe to streams (create listeners)
        self.ws.kline(symbol="BTCUSDT", interval="1s")
        self.ws.kline(symbol="LTCUSDT", interval="1s")


    def message_handler(self, _, msg):
        try:
            self.write(msg)
        except Exception as e:
            print("skipped write")
            pass 


    def write(self, msg):
        message = json.loads(msg)
        file_name = f"{message["stream"]}.parquet.snappy"
        path = os.path.join("data", file_name)

        # Match the attributes return by stream to Rest API vocab
        att = ["t", "o", "h", "l", "c", "v", "T", "q", "n", "V", "Q", "B"]
        columns = ["Open time", 
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
                   "Ignore"]
        temp = dict()
        i = 0
        for a in att:
            col = columns[i]
            temp_message = message["data"]["k"][a]
            if a == "t" or a == "T":
                temp[col] = int(temp_message)
            else:
                temp[col] = float(temp_message)
            i += 1

        print(temp)
        
        data = pd.DataFrame(temp, index=[0]) 
        data.to_parquet(path, compression="snappy")
        print(f"File {file_name} has been written.")
        print(Database.read("ltcusdt@kline_1s.parquet.snappy"))


if __name__ == "__main__":
    ws = Realtime()
    time.sleep(2)
    ws.ws.stop()
    print(Database.read("ltcusdt@kline_1s.parquet.snappy"))
