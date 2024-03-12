from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import pandas as pd
import os
import time

class Realtime():
    def __init__(self):
        self.ws = SpotWebsocketStreamClient(on_message=self.message_handler,
                                            is_combined=True,
                                            timeout=2)
        
        # Subscibe to streams (create listeners)
        self.ws.kline(symbol="BTCUSDT", interval="1s")
        self.ws.kline(symbol="LTCUSDT", interval="1s")


    def message_handler(self, _, msg):
        print(msg)


if __name__ == "__main__":
    ws = Realtime()
    time.sleep(10)
    ws.ws.stop()
