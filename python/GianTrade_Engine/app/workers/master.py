from db.db_manager import DBManager
from workers.user_manager import UserManager
from workers.trade_executer import TradeExec
from workers.activity_watcher import ActivityWatch
from private.strategies.one_m_5_d import OM5D 

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
            self.__db = DBManager(self.__db_name, dbuname, dbpass, self.__host, self.__port)
        self.__uManager = UserManager(self.__db)
        self.__actWatch= ActivityWatch(self.__db) 

        self.__strategies = {"OM5D":OM5D}
        self.__strategies_user_dict = {}

        
    def start_strategy(self, strategy_name, uname, pair):
        s = self.__strategies[strategy_name](self, uname, pair)
        s.start()
        # self.__strategies_user_dict.update({str(strategy_name)+uname+pair:s})
        self.__strategies_user_dict.update({uname:{strategy_name:{pair:s}}})
        return True
    
    def stop_strategy(self, strategy_name, uname, pair):
        try:
            # self.__strategies_user_dict[str(strategy_name)+uname+pair].stop()
            self.__strategies_user_dict[uname][strategy_name][pair].stop()
            self.__strategies_user_dict[uname][strategy_name].pop(pair)
            return True
        except:
            return False

    def get_all_strategies(self):
        return list(self.__strategies.keys())
    
    def get_strategy_log(self, strategy_name, uname, pair):
        try:
            return self.__strategies_user_dict[uname][strategy_name][pair].get_log()
        except:
            return False
    
    def get_running_strategies(self, uname):
        running = {}
        for strategy in list(self.__strategies_user_dict[uname].keys()):
            for pair in list(self.__strategies_user_dict[uname][strategy].keys()):
                running.update({strategy:pair})
        return running


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
        with self.__actWatch.record() as rec:
            self.__open_user_accounts[uname].buy_limit(pair, amount, price)
            rec.update({"uname":uname, "action":"BUY", "pair":pair, 
                        "amount":amount, "price":price, "fee":fee})

    def sell_lim_user(self, uname, pair, amount, price, fee=0.1):
        with self.__actWatch.record() as rec:
            self.__open_user_accounts[uname].sell_limit(pair, amount, price)
            rec.update({"uname":uname, "action":"SELL", "pair":pair, 
                        "amount":amount, "price":price, "fee":fee})

    def cancel_user_order(self, uname, pair, orderId, amount, price, fee=0.1):
        with self.__actWatch.record() as rec:
            self.__open_user_accounts[uname].cancel_order(pair, orderId)
            rec.update({"uname":uname, "action":"CANCEL", "pair":pair, 
                        "amount":amount, "price":price, "fee":fee})
    def get_user_pair_fee(self, uname, pair):
        return self.__open_user_accounts[uname].get_pair_fees(pair)
    
