from binance.client import Client
from binance.websockets import BinanceSocketManager
import time

class BinanceCom:
    def __init__(self):
        self.default_Key="api_key"
        self.default_Secret="api_secret"
        self.second_limit = 10
        self.minute_limit = 1200
        self.day_limit = 200000
        self._last_req_time = None
        self._sec_req_count = 0
        self._min_req_count = 0
        self._day_req_count = 0

    def _allow_execut(self, count, limit, now, secs, whatlimit=""):
        execute = False
        if self._last_req_time==None:
                 self._last_req_time=now
        if count<limit:
            count+=1
            execute=True
        elif now - self._last_req_time > secs:
            count=0
        else:
            print(f"{whatlimit} Limit reached !")
        return execute, count

    def watch_limit(func):
        def inner(self, *args, **kwargs):
            now = time.time()
            execute, self._sec_req_count =self._allow_execut(self._sec_req_count, self.second_limit, now, 1, "Second")
            execute, self._min_req_count =self._allow_execut(self._min_req_count, self.minute_limit, now, 60, "Minute")
            execute, self._day_req_count =self._allow_execut(self._day_req_count, self.day_limit, now, 86400, "Day")
    
            if execute:
                return func(self, *args, **kwargs)
                self._last_req_time=time.time()
            else:
                raise Exception("Exchange request limit reached!")
        return inner

    def set_last_req_time(self, timeinseconds):
        timeinseconds = int(timeinseconds)
        self._last_req_time=timeinseconds

    @watch_limit    
    def update_request_limits(self, client):
        rates = client.get_exchange_info()['rateLimits']
        for item in rates:
            if item['interval']=='SECOND':
                self.second_limit=int(item['limit'])
            if item['interval']=='MINUTE':
                self.minute_limit=int(item['limit'])
            if item['interval']=='DAY':
                self.day_limit=int(item['limit'])
        print(f"sec-{self.second_limit}, min-{self.minute_limit}, day-{self.day_limit}")

    def connect_to_account(self, apiKey, apiSecret):
        if apiKey==apiSecret==None:
            raise ValueError("Received 'None' argument.")
        return Client(apiKey, apiSecret)
    
    @watch_limit
    def get_coin_info(self, client, pair):
        return client.get_ticker(symbol=pair)
    
    @watch_limit
    def get_server_time(self, client):
        return client.get_server_time()
    
    def get_default_pairs(self):
        return ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']

    @watch_limit
    def get_wallet(self, client):
        content = client.get_account()['balances']
        available_balances = {}
        for item in content:
            if float(item['free'])+float(item['locked'])> 0.0:
                available_balances.update({item['asset']:[{'free':item['free']}, {'locked':item['locked']}]})
        return available_balances
    
    @watch_limit
    def get_open_orders(self, client):
        content = client.get_open_orders()
        features_to_include = ['orderId', 'price', 'origQty', 'executedQty', 'type', 'side', 'stopPrice']
        orders = {}
        for item in content:
            data = []
            for feature in features_to_include:
                data.append({feature:item[feature]})
            orders.update({item['symbol']:data})
        return orders
    
    
    
    
if __name__ == "__main__":
    bc = BinanceCom()
    # Create client which will send requests to exchange, default values will not enable trading.
    client = bc.connect_to_account(bc.default_Key, bc.default_Secret)
    # Get exchange request limits, values will be members of the class.
    bc.update_request_limits(client)
    # Get wallet content only assets with value will be presented.
    print("\n",bc.get_wallet(client))
    # Get open orders
    print("\n", bc.get_open_orders(client))
    