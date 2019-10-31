from db.db_manager import DBManager
from workers.user_manager import UserManager
from workers.trade_executer import TradeExec
from workers.activity_watcher import ActivityWatch

class Master:
    def __init__(self, dbuname, dbpass):
        self.TAG = "Master >> "
        self.__db_name = "gianttrade"
        self.__host = "docker_db_1"
        self.__port = "5432"
        self.__open_user_accounts = {}

        self.__db = DBManager(self.__db_name, dbuname, dbpass, self.__host, self.__port)
        self.__uManager = UserManager(self.__db)
        self.__actWatch= ActivityWatch() 
        
        
        
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
        return self.__open_user_accounts[uname].get_ohlcv(pair, for_num_of_days)

    def buy_lim_user(self, uname, pair, amount, price):
        self.__open_user_accounts[uname].buy_limit(pair, amount, price)

    def sell_lim_user(self, uname, pair, amount, price):
        self.__open_user_accounts[uname].sell_limit(pair, amount, price)

    def cencel_user_order(self, uname, pair, orderId):
        self.__open_user_accounts[uname].cancel_order(pair, orderId)
    
