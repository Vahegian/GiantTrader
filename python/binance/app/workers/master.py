from db.db_manager import DBManager
from workers.user_manager import UserManager
from workers.trade_executer import TradeExec
from workers.activity_watcher import ActivityWatch

class Master:
    def __init__(self, dbuname=None, dbpass=None, dbFile=None):
        self.TAG = "Master >> "
        self.__db_name = "gianttrade"
        self.__host = "docker_db_1"
        self.__port = "5432"
        self.__open_user_accounts = {}
        if dbFile != None:
            self.__db = DBManager(db_file=dbFile)
        else:
            self.__db = DBManager()
        self.__uManager = UserManager(self.__db)
        self.__actWatch= ActivityWatch(self.__db) 

    def get_user_data(self, uname, password):
        '''
            returns an array containing user details. 
        '''
        return self.__uManager.get_user_info(uname, password)

    def open_user_account(self, uname, apiKey, apiSecret):
        '''
            Creates a TradeExec class object with supplied apiKey and Secret.
            The object is stored in a dictionary where key is the supplied user name.
        '''
        if uname in list(self.__open_user_accounts.keys()):
            print(self.TAG, "User Exists!")
            return
        self.__open_user_accounts.update({uname.strip(): TradeExec(apiKey.strip(),
                                         apiSecret.strip(), self.__actWatch)})
    def close_user_account(self, uname):
        uname = uname.strip()
        self.__open_user_accounts[uname] = None
        self.__open_user_accounts.pop(uname)

    def add_user(self, uname, password, apiKey, secret):
        self.__uManager.add_user(uname, password, apiKey, secret)

    def get_all_users(self):
        return [u for u in list(self.__open_user_accounts.keys())]
    
    def get_user_wallet(self, uname):
        return self.__open_user_accounts[uname].update_wallet()  

    def get_user_open_orders(self, uname):
        return self.__open_user_accounts[uname].update_open_orders()

    def get_user_last_prices(self, uname):
        return self.__open_user_accounts[uname].get_last_prices()

    def get_user_ohlcv(self, uname, pair, for_num_of_days=7):
        return self.__open_user_accounts[uname].get_ohlcv(pair, for_num_of_days-1)

    def buy_lim_user(self, uname, pair, amount, price, fee=0.1):
        resp = self.__open_user_accounts[uname].buy_limit(pair, amount, price)
        print(self.TAG, "buy lim user" ,resp, resp['symbol'],pair,resp['status'], "NEW", resp['price'])
        if pair==resp['symbol'] and resp['status']=="NEW":
            with self.__actWatch.record() as rec:
                rec.update({"uname":uname, "action":"BUY", "pair":resp['symbol'], 
                        "amount":resp['origQty'], "price":resp['price'], "fee":fee})
            return True
        return False

    def sell_lim_user(self, uname, pair, amount, price, fee=0.1):
        resp = self.__open_user_accounts[uname].sell_limit(pair, amount, price)
        print(self.TAG, "sell lim user" ,resp, resp['symbol'],pair,resp['status'], "NEW", resp['price'])
        if pair==resp['symbol'] and resp['status']=="NEW":
            with self.__actWatch.record() as rec:
                rec.update({"uname":uname, "action":"SELL", "pair":resp['symbol'], 
                        "amount":resp['origQty'], "price":resp['price'], "fee":fee})
            return True
        return False

    def buy_user(self, uname, pair, amount, fee=0.1):
        resp = self.__open_user_accounts[uname].buy_market(pair, amount)
        print(self.TAG, "buy user" ,resp, resp['symbol'],pair,resp['status'], "FILLED", resp['price'])
        if pair==resp['symbol'] and resp['status']=="FILLED":
            price = 0.0
            for item in resp['fills']:
                temp_price = float(item['price'])
                if temp_price>price:
                    price = temp_price
            with self.__actWatch.record() as rec:
                rec.update({"uname":uname, "action":"BUY", "pair":resp['symbol'], 
                        "amount":resp['origQty'], "price":resp['price'], "fee":fee})
            return True, price
        return False, 0

    def sell_user(self, uname, pair, amount, fee=0.1):
        resp = self.__open_user_accounts[uname].sell_market(pair, amount)
        print(self.TAG, "sell user" ,resp, resp['symbol'],pair,resp['status'], "FILLED", resp['price'])
        if pair==resp['symbol'] and resp['status']=="FILLED":
            price = 0.0
            for item in resp['fills']:
                temp_price = float(item['price'])
                if temp_price>price:
                    price = temp_price
            with self.__actWatch.record() as rec:
                rec.update({"uname":uname, "action":"SELL", "pair":resp['symbol'], 
                        "amount":resp['origQty'], "price":resp['price'], "fee":fee})
            return True, price
        return False, 0

    def cancel_user_order(self, uname, pair, orderId, amount, price, fee=0.1):
        resp = self.__open_user_accounts[uname].cancel_order(pair, orderId)
        print(resp)
        if int(orderId)==int(resp['orderId']) and resp["status"]=="CANCELED":
            with self.__actWatch.record() as rec:
                rec.update({"uname":uname, "action":"CANCEL", "pair":resp['symbol'], 
                        "amount":resp['origQty'], "price":resp['price'], "fee":fee})
            return True
        return False

    def get_user_pair_fee(self, uname, pair):
        return self.__open_user_accounts[uname].get_pair_fees(pair)
    
