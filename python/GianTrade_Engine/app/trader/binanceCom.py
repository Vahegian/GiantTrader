from binance.client import Client
from binance.websockets import BinanceSocketManager

class BinanceCom:
    def __init__(self):
        self.default_Key="api_key"
        self.default_Secret="api_secret"
        self.second_limit = 10
        self.minute_limit = 1200
        self.day_limit = 100000

    def connect_to_account(self, apiKey, apiSecret):
        if apiKey==apiSecret==None:
            raise ValueError("Received 'None' argument.")
        return Client(apiKey, apiSecret)

    def get_coin_info(self, client, pair):
        return client.get_ticker(symbol=pair)

    def get_server_time(self, client):
        return client.get_server_time()
    
    def get_default_pairs(self):
        return ['BTCUSDT', 'ETHUSDT', 'XRPUSDT',]
    
    
if __name__ == "__main__":
    bc = BinanceCom()
    client = bc.connect_to_account(bc.default_Key, bc.default_Secret)
    print(bc.get_coin_info(client, "BTCUSDT"))