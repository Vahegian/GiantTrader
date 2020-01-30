from bots.rolling_day_trader import RollingDayTrader
class Master:
    def __init__(self):
        self.bots = {"RollingDayTrader11/1.5/2.0":[11, 1.5, 2.0],
                     "RollingDayTrader11/1.5/1.0":[11, 1.1, 1.5],
                     "RollingDayTrader15/1.5/2.0":[15, 1.5, 2.0],
                     "RollingDayTrader20/1.5/2.0":[20, 1.5, 2.0],
                     "RollingDayTrader11/1.5/1.0":[11, 1.5, 1.0]}
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
            bot = RollingDayTrader(uname, pair, minUSDT=bot_params[0], wantedProfitPercent=bot_params[1], maxAcceptableLossPercent=bot_params[2])
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
