from bots.BOT import BOT
import threading
from bots.exchanges.binance import BinanceAPI
import datetime
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
        self.__maxFee = 0.2 # %
        self.__current_amount_usd = 0.0
        self.__profit_last_trade = 0.0

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
    
    def get_bot_info(self):
        ls = self.__price_bought-((self.__loss_percent/100)*self.__price_bought) #loss sell price
        ps = self.__price_bought+((self.__profit_percent/100)*self.__price_bought)
        return {"bot":self.__TAG, "pair":self.__pair, "minUSDT":f"{self.__min_USDT:.6f}", "profitPercent":self.__profit_percent, "lossPercent":self.__loss_percent,
                "updateInterval":self.__update_interval_sec, "amountBought":f"{self.__amount_bought:.6f}", "priceBought":f"{self.__price_bought:.6f}", "lsps":f"{ls:.6f}/{ps:.6f}",
                "lt_profit": f"{self.__profit_last_trade:.6f}", "lt_profit_p":f"{self.__getProfit():.2f}", "total_usdt": f"{self.__current_amount_usd:.6f}"}

    def __getProfit(self):
        if (self.__amount_bought*self.__price_bought) > 0.0:
            return self.__profit_last_trade/(self.__amount_bought*self.__price_bought)
        else:
            return 0.0

    def __start_thrading(self):
        with self.__bot_thread_lock:
            run = self.__isRunning
        while run:
            self.__trade()
            time.sleep(self.__update_interval_sec)
            with self.__bot_thread_lock:
                run = self.__isRunning

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
        success, price = self.__binance.buy_market(self.__pair,f"{amount:.6f}")
        print(self.__TAG, "buy usdt", success, price, amount)
        if success:
            self.__save_bought_time()
            self.__price_bought = price
            self.__amount_bought = amount
            self.__add_log_at_date_time(f"Bought {amount} {self.__pair} at {price} on {self.__bought_time}")
        else:
            self.__add_log_at_date_time(f"Failed to Buy {amount} {self.__pair} at {price} on {self.__get_cur_time()}")

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
        self.__sell_at_percent_diff(curPrice, self.__loss_percent)

    def __sell_percent_profit(self, curPrice):
        self.__add_log_at_date_time(f"Trying to sell {self.__profit_percent} percent at profit for {self.__pair} ")
        self.__sell_at_percent_diff(curPrice, self.__profit_percent)

    def __sell_at_percent_diff(self, curPrice, percent):
        percent_diff = self.__get_percent_diff_from_bought_price(curPrice)
        self.__add_log_at_date_time(f"Percent difference is {percent_diff} and percent to sell at is {percent}")
        if percent_diff >= percent:
            sellable_amount = self.__amount_bought - ((self.__maxFee/100) * self.__amount_bought)
            success, price = self.__binance.sell_market(self.__pair, f"{sellable_amount:.6f}")
            self.__add_log_at_date_time(f"closing the order at price {curPrice} and percent difference is {percent_diff}")
            print(self.__TAG, "sell percent", success, price, curPrice, percent, percent_diff)
            if success:
                self.__add_log_at_date_time(f"Sold {sellable_amount} {self.__pair} at {price} on {self.__get_cur_time()}, percent_diff {percent_diff}%")
                self.__add_log_at_date_time(f"waiting {self.__seconds_to_wait_after_sell} seconds")
                self.__profit_last_trade =(price*self.__amount_bought) - (self.__amount_bought*self.__price_bought)
                time.sleep(self.__seconds_to_wait_after_sell)
                self.__amount_bought = 0
                

    def __close_position_if_new_day(self, curPrice):
        self.__add_log_at_date_time(f"Trying to close the position for {self.__pair} at price {curPrice} if it is the next day")  
        isNextDay, isPassBoughtTime = False, False      
        curTime  = self.__get_cur_time()
        if self.__bought_time.day < curTime.day:
            isNextDay = True
            self.__add_log_at_date_time(f"It is the next day!")
        else:
            self.__add_log_at_date_time(f"next day {self.__bought_time.day < curTime.day} !")

        if  self.__bought_time.hour <= curTime.hour and self.__bought_time.minute <= curTime.minute:
            isPassBoughtTime = True 
            self.__add_log_at_date_time(f"It is pass buy time!")
        else:
            self.__add_log_at_date_time(f"pass bought hour = { self.__bought_time.hour < curTime.hour} | pass bought minute = {self.__bought_time.minute < curTime.minute}!")

        self.__add_log_at_date_time(f"Current time {curTime} time of purchase {self.__bought_time}") 
        if isNextDay and isPassBoughtTime:
            self.__add_log_at_date_time(f"Selling now because it is the next day") 
            self.__sell_at_percent_diff(curPrice, 0.0)
            # percent_diff = self.__get_percent_diff_from_bought_price(curPrice)
            # self.__add_log_at_date_time(f"closing the day at price {curPrice} and percent difference is {percent_diff}")
            # sellable_amount = self.__amount_bought - ((self.__maxFee/100) * self.__amount_bought)
            # success, price = self.__binance.sell_market(self.__pair, f"{sellable_amount:.6f}")
            # if success:
            #     self.__add_log_at_date_time(f"Sold {sellable_amount} {self.__pair} at {price} on {self.__get_cur_time()}, percent_diff {percent_diff}%")
            #     time.sleep(self.__seconds_to_wait_after_sell)
            #     self.__amount_bought = 0


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
