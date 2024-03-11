from binance.spot import Spot

class BinanceAPI():
    def __init__(self):
        self.client = Spot()
    

    def get_klines(self, symbol, interval):
        return self.client.klines(symbol, interval)
    

    def get_klines_limit(self, symbol, interval, limit):
        return self.client.klines(symbol, interval, limit=limit)