from trader.trader import Trader

class TradeExec:
    def __init__(self, apiKey, apiSecret, activityWatcher):
        self.TAG = "TradeExec >> "
        self.__trader = Trader()
        self.__aw = activityWatcher

        connected = self.__trader.connect_to_account(apiKey, apiSecret)
        if not connected:
            raise ValueError(self.TAG, "ApiKey or Secret is Not Valid")
        self.__trader.update_request_limits()
        self.fees = self.__trader.get_fees()
        
        self.__wallet = None
        # self.__openOrders = []
        self.__prices = {}
        self.start_price_tickers()
        # self.__trader.market_buy("XRPUSDT", 10)
        # exit(0)


    def update_wallet(self):
        self.__wallet = self.__trader.get_wallet()
        return self.__wallet
    
    def update_open_orders(self):
        self.__openOrders = self.__trader.get_open_orders()
        for item in self.__openOrders:
            item.update({"fee":float(self.get_pair_fees(item["symbol"])["taker"])*100})
        return self.__openOrders

    def buy_limit(self, pair, amount, price):
        return self.__trader.put_limit_order_buy(pair, amount, price)
       
    def sell_limit(self, pair, amount, price):
        return self.__trader.put_limit_order_sell(pair, amount, price)
        
    def buy_market(self, pair, amount):
        return self.__trader.market_buy(pair, amount)

    def sell_market(self, pair, amount):
        return self.__trader.market_sell(pair, amount)

    def cancel_order(self, pair, orderId):
        return self.__trader.cancel_order(pair, orderId)

    def start_price_tickers(self):
        self.__trader.get_live_ticker_update(self.__update_prices)

    def __update_prices(self, msg):
        for item in msg:
            self.__prices.update({item['s']: item['c']})
    
    def get_last_prices(self):
        return self.__prices

    def get_ohlcv(self, pair, for_num_of_days):
        return self.__trader.get_hist_data_day_interval(pair, for_num_of_days)
    
    def get_pair_fees(self, pair):
        if self.fees != None:
            for item in self.fees["tradeFee"]:
                if item["symbol"] == pair:
                    return item
        else:
            return False
    
    def close_account(self):
        return self.__trader.close_account()

