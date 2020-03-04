from bots.rolling_day_trader import RollingDayTrader
class Master:
    def __init__(self):
        self.bots = {
                     "RollingDayTrader10.2/0.6/0.4":[10.2, 0.6, 0.4,True],
                     "RollingDayTrader10.2/0.6/inf":[10.2, 0.6, 1000,True],
                     "RollingDayTrader10.2/1.0/1.0":[10.2, 1.0, 1.0,True],
                     "RollingDayTrader10.2/1.0/1.5":[10.2, 1.0, 1.5,True],
                     "RollingDayTrader10.2/1.5/inf":[10.2, 1.5, 1000,True],
                     "RollingDayTrader10.2/5.0/inf/NF":[10.2, 5.0, 1000,False],
                     "RollingDayTrader10.2/10.0/inf/NF":[10.2, 10.0, 1000,False],
                     "RollingDayTrader11/1.0/1.0":[11, 1.0, 1.0,True],
                     "RollingDayTrader11/1.0/1.5":[11, 1.0, 1.5,True],
                     "RollingDayTrader11/1.5/1.0":[11, 1.5, 1.0,True],
                     "RollingDayTrader11/1.5/2.0":[11, 1.5, 2.0,True],
                     "RollingDayTrader15/0.6/inf":[15, 0.6, 1000,True],
                     "RollingDayTrader15/1.0/1.5":[15, 1.0, 1.5,True],
                     "RollingDayTrader15/1.5/2.0":[15, 1.5, 2.0,True],
                     "RollingDayTrader15/5.0/inf/NF":[15, 5.0, 1000,False],
                     "RollingDayTrader15/10.0/inf/NF":[15, 10.0, 1000,False],
                     "RollingDayTrader20/1.0/1.5":[20, 1.0, 1.5,True],
                     "RollingDayTrader20/0.6/inf":[20, 0.6, 1000,True],
                     "RollingDayTrader20/1.5/2.0":[20, 1.5, 2.0,True],
                     "RollingDayTrader20/5.0/inf/NF":[20, 5.0, 1000,False],
                     "RollingDayTrader20/10.0/inf/NF":[20, 10.0, 1000,False],
                     "RollingDayTrader50/0.6/inf":[50, 0.6, 1000,True],
                     "RollingDayTrader50/1.0/1.5":[50, 1.0, 1.5,True],
                     "RollingDayTrader50/5.0/inf/NF":[50, 5.0, 1000,False],
                     "RollingDayTrader50/10.0/inf/NF":[50, 10.0, 1000,False],
                     "RollingDayTrader100/0.6/inf":[100, 0.6, 1000,True],
                     "RollingDayTrader100/1.0/1.5":[100, 1.0, 1.5,True]
                     }
        self.running_bots = {}
        self.__id = 0

    def get_all_bots(self):
        return list(self.bots.keys())

    def get_running_bots(self):
        content = []
        for item in list(self.running_bots.keys()):
            bot_data = self.running_bots[item].get_bot_info()
            content.append([item, bot_data])
        return content

    def start_bot(self, pair, bot_name, uname):
        if bot_name in self.get_all_bots():
            bot_params = self.bots[bot_name]
            bot = RollingDayTrader(uname, pair, minUSDT=bot_params[0], wantedProfitPercent=bot_params[1], maxAcceptableLossPercent=bot_params[2], close_next_day=bot_params[3])
            # bot.set_bot_params(uname, pair)
            if bot.start():
                self.__id +=1
                self.running_bots.update({self.__id:bot})
                return self.__id
        return False
    
    def stop_bot(self, bid):
        bid = int(bid)
        if bid in list(self.running_bots.keys()):
            if self.running_bots[bid].stop():
                self.running_bots.pop(bid)
                return True
        return False

    def get_running_bot_info(self, bid):
        bid = int(bid)
        if bid in list(self.running_bots.keys()):
            # print(bid, list(self.running_bots.keys()))
            return self.running_bots[bid].get_log()
        return False
