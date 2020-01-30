from binance.client import Client
from binance.websockets import BinanceSocketManager
import time
from datetime import date, timedelta

class Trader:
    def __init__(self):
        self.default_Key="api_key"
        self.default_Secret="api_secret"
        self._client = None
        self.second_limit = 10
        self.minute_limit = 1200
        self.day_limit = 200000
        self._last_req_time = None
        self._sec_req_count = 0
        self._min_req_count = 0
        self._day_req_count = 0
        self.__bm = None
        # self.min_amount_allowed_USD=10.0

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

    def check_client(func):
        def inner(self, *args, **kwargs):
            if self._client!=None:
                return func(self, *args, **kwargs)
            else:
                print("Operation is not complete, connect to client")
        return inner

    def set_last_req_time(self, timeinseconds):
        timeinseconds = int(timeinseconds)
        self._last_req_time=timeinseconds

    @watch_limit 
    @check_client
    def get_fees(self):
        return self._client.get_trade_fee()
        

    @watch_limit 
    @check_client   
    def update_request_limits(self):
        rates = self._client.get_exchange_info()['rateLimits']
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
        self._client = Client(apiKey, apiSecret)
        return True
    
    @watch_limit
    @check_client
    def get_coin_info(self, pair):
        return self._client.get_ticker(symbol=pair)
    
    @watch_limit
    @check_client
    def get_server_time(self):
        return self._client.get_server_time()
    
    def get_default_pairs(self):
        return ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']

    @watch_limit
    @check_client
    def get_wallet(self):
        content = self._client.get_account()['balances']
        available_balances = {}
        for item in content:
            if float(item['free'])+float(item['locked'])> 0.0:
                data = {}
                data.update({'free':item['free']})
                data.update({'locked':item['locked']})
                available_balances.update({item['asset']:data})
        return available_balances
    
    @watch_limit
    @check_client
    def get_open_orders(self):
        content = self._client.get_open_orders()
        features_to_include = ['symbol', 'orderId', 'price', 'origQty', 'executedQty', 'type', 'side', 'stopPrice']
        orders = []
        for item in content:
            data = {}
            for feature in features_to_include:
                data.update({feature:item[feature]})
            orders.append(data)
        return orders

    @watch_limit
    @check_client
    def cancel_order(self, symbol, orderId):
        if int(orderId) != None and symbol !=None:
            return self._client.cancel_order(symbol=symbol, orderId=orderId)
    
    @watch_limit
    @check_client
    def put_limit_order_buy(self, symbol, quantity, price):
        if symbol!=None and float(quantity) != None and float(price) != None:
            # if quantity*price>self.min_amount_allowed_USD:
            return self._client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)   

    @watch_limit
    @check_client
    def put_limit_order_sell(self, symbol, quantity, price):
        if symbol!=None and float(quantity) != None and float(price) != None:
            # if quantity*price>self.min_amount_allowed_USD:
            return self._client.order_limit_sell(symbol=symbol, quantity=quantity, price=price) 

    @watch_limit
    @check_client
    def get_live_ticker_update(self, callback):
        self.__bm = BinanceSocketManager(self._client)
        self.__bm.start_ticker_socket(callback=callback)
        self.__bm.start()

    @watch_limit
    @check_client
    def get_hist_data_day_interval(self, symbol, numofdays):
        d = date.today() - timedelta(days=int(numofdays))
        content = self._client.get_historical_klines(symbol ,self._client.KLINE_INTERVAL_1DAY, str(d)+" UTC", limit=1000)
        data = {}
        for item in content:
            item_date = str(date.fromtimestamp(int(item[0]/1000)))
            item_content = {"open":item[1],
                            "high":item[2],
                            "low":item[3],
                            "close":item[4],
                            "volume":item[5]}
            data.update({item_date: item_content})
        return data
    
    @check_client
    def close_account(self):
        self.__bm.close()
        self._client = None
        return True

    @watch_limit
    @check_client
    def market_sell(self, symbol, quantity):
        if symbol!=None and float(quantity) != None:
            # if quantity*price>self.min_amount_allowed_USD: 
            return self._client.order_market_sell(symbol=symbol, quantity=quantity)
    
    @watch_limit
    @check_client
    def market_buy(self, symbol, quantity):
        if symbol!=None and float(quantity) != None:
            # if quantity*price>self.min_amount_allowed_USD: 
            return self._client.order_market_buy(symbol=symbol, quantity=quantity) 

if __name__ == "__main__":
    bc = Trader()
    # Create client which will send requests to exchange, default values will not enable trading.
    isConected = bc.connect_to_account(bc.default_Key, bc.default_Secret)
    # Get exchange request limits, values will be members of the class.
    bc.update_request_limits()
    # Get wallet content only assets with value will be presented.
    print("\n",bc.get_wallet())
    # Get open orders
    oOrder = bc.get_open_orders()
    print("\n", oOrder)
    # Cancel an active order
    # print("\n", bc.cancel_order('XRPUSDC', oOrder['XRPUSDC']['orderId']))

    #put sell limit order
    # print(bc.put_limit_order_sell("XRPUSDT", 31.6, 0.48))
    
    # # get live update from web socket
    # p = lambda msg: print(msg[0]['s'], msg[0]['p'])
    # bc.get_live_ticker_update(p)

    #get historical OHLCV data
    print("\n", bc.get_hist_data_day_interval("XRPUSDT", 3))

    
    