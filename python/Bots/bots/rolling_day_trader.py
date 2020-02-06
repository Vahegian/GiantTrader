from bots.BOT import BOT
import threading
from bots.exchanges.binance import BinanceAPI
import datetime
from datetime import timedelta
import time


class RollingDayTrader(BOT):
    def __init__(self, user, pair, minUSDT=11.0, wantedProfitPercent=1.5, maxAcceptableLossPercent=2.0, updateSec=5):
        super(RollingDayTrader, self).__init__()
        self.__TAG = "RollingDayTrader"
        self.__pair = pair
        self.__bot_thread = None
        self.__bot_thread_lock = threading.Lock()
        self.__isRunning = False
        self.__binance = BinanceAPI(user)
        self.__price_bought = 0.0
        self.__bought_time = None
        self.__amount_bought = 0.0
        self.__add_log_at_date_time(f"Init {self.__TAG} with {minUSDT}, {wantedProfitPercent}, {maxAcceptableLossPercent}")
        self.__min_USDT = float(minUSDT)
        self.__profit_percent = float(wantedProfitPercent)
        self.__loss_percent = float(maxAcceptableLossPercent)
        self.__update_interval_sec = int(updateSec)
        self.__seconds_to_wait_after_sell = int(2.5*60)
        self.__maxFee = 0.25 # %
        self.__current_amount_usd = 0.0
        self.__profit_last_trade = 0.0
        # cool down for too much loosing variables
        self.__num_of_profit_trades = 0
        self.__num_of_loss_trades = 0
        self.__time_of_losses = None
        self.__num_allowed_losses = 1
        self.__delay_after_losses = 5 #hours 
        self.__loss_window = []
        self.__isCooling = False

        self.__order_acc = 6 #decimal places
        self.__pair_acc = {"ETHUSDT":4, "BCHUSDT":4, "XRPUSDT":1, "LTCUSDT":4}
        self.__set_order_acc()

    def start(self):
        try:
            self.__isRunning = True
            self.__bot_thread = threading.Thread(target=self.__start_thrading)
            self.__bot_thread.start()
            return True
        except:
            return False

    def stop(self):
        try:
            with self.__bot_thread_lock:
                self.__isRunning = False
            self.__bot_thread.join()
            return True
        except:
            return False

    def __set_order_acc(self):
        if self.__pair in list(self.__pair_acc.keys()):
            self.__order_acc = self.__pair_acc[self.__pair]
    
    def get_bot_info(self):
        loss_sell = self.__price_bought-((self.__loss_percent/100)*self.__price_bought) #loss sell price
        profit_sell = self.__price_bought+((self.__profit_percent/100)*self.__price_bought)
        loss_percent, profit_percent = self.get_loss_and_profit_over_total() 
        return {"bot":self.__TAG, "pair":self.__pair, "minUSDT":f"{self.__min_USDT:.6f}", "profitPercent":self.__profit_percent, "lossPercent":self.__loss_percent,
                "updateInterval":self.__update_interval_sec, "amountBought":f"{self.__amount_bought:.6f}", "priceBought":f"{self.__price_bought:.6f}", 
                "lsps":f"{loss_sell:.6f}/{profit_sell:.6f}", "lt_profit": f"{self.__profit_last_trade:.6f}", "lt_profit_p":f"{self.__getProfit():.2f}",
                "total_usdt": f"{self.__current_amount_usd:.6f}", "lnum": self.__num_of_loss_trades, "pnum":self.__num_of_profit_trades, "l_percent":f"{loss_percent:.2f}",
                "p_percent":f"{profit_percent:.2f}"}

    def __getProfit(self):
        if (self.__amount_bought*self.__price_bought) > 0.0:
            return (self.__profit_last_trade/(self.__amount_bought*self.__price_bought))*100
        else:
            return 0.0

    def get_loss_and_profit_over_total(self):
        loss_p = 0.0
        profit_p = 0.0
        total = self.__num_of_loss_trades+self.__num_of_profit_trades
        if total == 0:
            return loss_p, profit_p
        loss_p = (self.__num_of_loss_trades/total)*100
        profit_p = (self.__num_of_profit_trades/total)*100
        return loss_p, profit_p


    def __start_thrading(self):
        with self.__bot_thread_lock:
            run = self.__isRunning
        while run:
            self.__add_log_at_date_time("New Iteration ...")
            self.__cool_down()
            if self.__time_of_losses == None:
                self.__trade()
            time.sleep(self.__update_interval_sec)
            with self.__bot_thread_lock:
                run = self.__isRunning

    def __cool_down(self):
        if len(self.__loss_window)==self.__num_allowed_losses and self.__time_of_losses==None:
            self.__time_of_losses = self.__get_cur_time()
        
        if self.__time_of_losses != None:
            temp_time = self.__time_of_losses+timedelta(hours=self.__delay_after_losses)
            time_now = self.__get_cur_time()
            if time_now >= temp_time:
                self.__time_of_losses = None
                self.__loss_window = []
            else:
                self.__add_log_at_date_time(f"Cooling down after {len(self.__loss_window)} losses on {self.__time_of_losses}")
                time.sleep(60)
        
    def __trade(self):
        price = self.__check_cur_price()
        if price:
            if self.__amount_bought <=0:
                if self.__check_resource_availability(): # two ifs to avoid having wallet checked when not necessary 
                    self.__buy_for_USDT(price)
            else:
                self.__add_log_at_date_time(f"Trying to sell {self.__amount_bought} {self.__pair}")
                if price > self.__price_bought:
                    self.__sell_percent_profit(price)
                else:
                    self.__sell_percent_loss(price)
                self.__close_position_if_new_day(price)
            self.__current_amount_usd = price*self.__amount_bought

    def __check_resource_availability(self):
        self.__add_log_at_date_time("Trying to get balance")
        balance = self.__binance.get_available_balance("USDT")
        self.__add_log_at_date_time(f"balance for \"USDT\" is {balance}")
        if balance >=self.__min_USDT:
            return True
        return False

    def __save_bought_time(self):
        self.__bought_time = self.__get_cur_time()

    def __buy_for_USDT(self, curPrice):
        self.__add_log_at_date_time(f"Trying to buy for {self.__min_USDT} USDT")
        amount = self.__min_USDT/curPrice
        success, price = self.__binance.buy_market(self.__pair, round(amount, self.__order_acc))
        print(self.__TAG, "buy usdt", success, price, amount)
        if success:
            self.__save_bought_time()
            self.__price_bought = price
            self.__amount_bought = amount
            self.__add_log_at_date_time(f"Bought {amount} {self.__pair} at {price} on {self.__bought_time}")
        else:
            self.__add_log_at_date_time(f"Failed to Buy {amount} {self.__pair} on {self.__get_cur_time()}")

    def __check_cur_price(self):
        self.__add_log_at_date_time(f"Checking current price for {self.__pair}")
        price = self.__binance.get_current_price(self.__pair)
        if price:
            return price
        else:
            print(self.__TAG, f"failed to fetch curent price for {self.__pair}")
            return False

    def __sell_percent_loss(self, curPrice):
        self.__add_log_at_date_time(f"Trying to sell {self.__loss_percent} percent at loss for {self.__pair} ")
        if self.__sell_at_percent_diff(curPrice, self.__loss_percent):
            self.__num_of_loss_trades+=1
            self.__loss_window.append(1)

    def __sell_percent_profit(self, curPrice):
        self.__add_log_at_date_time(f"Trying to sell {self.__profit_percent} percent at profit for {self.__pair} ")
        if self.__sell_at_percent_diff(curPrice, self.__profit_percent):
            self.__num_of_profit_trades+=1

    def __sell_at_percent_diff(self, curPrice, percent):
        success = False
        percent_diff = self.__get_percent_diff_from_bought_price(curPrice)
        self.__add_log_at_date_time(f"Percent difference is {percent_diff} and percent to sell at is {percent}")
        if percent_diff >= percent:
            sellable_amount = self.__amount_bought - ((self.__maxFee/100) * self.__amount_bought)
            success, price = self.__binance.sell_market(self.__pair, round(sellable_amount, self.__order_acc))
            self.__add_log_at_date_time(f"closing {sellable_amount} {self.__pair} at price {curPrice} and percent difference is {percent_diff}")
            print(self.__TAG, "sell percent", success, price, curPrice, percent, percent_diff)
            if success:
                self.__add_log_at_date_time(f"Sold {sellable_amount} {self.__pair} at {price} on {self.__get_cur_time()}, percent_diff {percent_diff}%")
                self.__profit_last_trade =(price*self.__amount_bought) - (self.__amount_bought*self.__price_bought)
                self.__add_log_at_date_time(f"waiting {self.__seconds_to_wait_after_sell} seconds ....")
                time.sleep(self.__seconds_to_wait_after_sell)
                self.__amount_bought = 0
        return success
                

    def __close_position_if_new_day(self, curPrice):
        self.__add_log_at_date_time(f"Trying to close the position for {self.__pair} at price {curPrice} if it is the next day")      
        tempTime = self.__bought_time + timedelta(days=1)
        curTime  = self.__get_cur_time()
        isNextDay = (curTime >= tempTime)
        self.__add_log_at_date_time(f"Next day=={isNextDay} :: Current time {curTime} time of purchase {self.__bought_time}")
        if isNextDay:
            self.__add_log_at_date_time(f"Selling now because it is the next day") 
            self.__sell_at_percent_diff(curPrice, 0.0)

    def __add_log_at_date_time(self, msg):
        data = [f"RollingDayTrader: log time {self.__get_cur_time()}", msg]
        self.add_log(data)

    def __get_cur_time(self):
        return datetime.datetime.now()

    def __get_percent_diff_from_bought_price(self, curPrice):
        diff = curPrice - self.__price_bought
        if diff < 0:
            diff = diff*-1
        percent_diff = (diff/self.__price_bought)*100
        return percent_diff

if __name__ == "__main__":
    r = RollingDayTrader("t", "1")
