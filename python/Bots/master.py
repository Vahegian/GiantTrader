from bots.rolling_day_trader import RollingDayTrader
class Master:
    def __init__(self):
        self.bots = {"RollingDayTrader":RollingDayTrader}
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
            bot = self.bots[bot_name](uname, pair)
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
