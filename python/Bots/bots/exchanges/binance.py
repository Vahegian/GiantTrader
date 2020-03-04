import requests
import json

class BinanceAPI:
    def __init__(self, username):
        self.__user = username
        self.__urls = {
            "server":"http://172.20.0.3:5000",
            "u_get_wallet_url": "/ud/wallet",
            "u_get_last_prices_url": "/lastprices",
            "u_sell_market_url": "/msell",
            "u_buy_market_url": "/mbuy"
        }

        self.__headers = {'Content-Type': 'application/json'}
        self.__TAG = "BinanceAPI"

    def get_current_price(self, pair):
        try:
            data = requests.post(url=self.__urls["server"]+self.__urls["u_get_last_prices_url"],
                                data= json.dumps({"uname":self.__user}),
                                headers=self.__headers)
            data = json.loads(data.text)[pair]
            return float(data)
        except Exception as e:
            print(self.__TAG,"get_current_price" ,e)
            return False

    def get_available_balance(self, symbol):
        try:
            data = requests.post(url=self.__urls["server"]+self.__urls["u_get_wallet_url"],
                                data= json.dumps({"uname":self.__user}),
                                headers=self.__headers)
            data = json.loads(data.text)
            amount = float(data[symbol]['free'])
            return amount
        except Exception as e:
            print(self.__TAG, "get_available_balance" ,e)
            return False

    def buy_market(self, pair, amount, fee=0.1):
        try:
            data = requests.post(url=self.__urls["server"]+self.__urls["u_buy_market_url"],
                                data= json.dumps({"uname":self.__user, "pair":pair, "amount":amount, "fee":fee}),
                                headers=self.__headers)
            data = json.loads(data.text)
            print(data)
            if int(data["status"])==1:
                return True, float(data["price"])
            return False, 0
        except Exception as e:
            print(self.__TAG, "buy_market" ,e.with_traceback())
            return False, 0

    def sell_market(self, pair, amount, fee=0.1):
        try:
            data = requests.post(url=self.__urls["server"]+self.__urls["u_sell_market_url"],
                                data= json.dumps({"uname":self.__user, "pair":pair, "amount":amount, "fee":fee}),
                                headers=self.__headers)
            data = json.loads(data.text)
            if int(data["status"])==1:
                return True, float(data["price"])
            return False, 0
        except Exception as e:
            print(self.__TAG,"sell_market" ,e.with_traceback())
            return False, 0
        

# if __name__ == "__main__":
    # b = BinanceAPI("vahe2nd")
    # print(b.get_current_price("BTCUSDT"))
    # print(b.get_available_balance("USDT"))
    # b.buy_market("XRPUSDT", 10)