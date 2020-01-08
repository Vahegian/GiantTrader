from bots.DNN9_T512_B2_D1_Q120 import DNN9_T512_B2_D1_Q120_Bot
class Master:
    def __init__(self):
        self.bots = {"DNN9-T512-B2-D1-Q120":DNN9_T512_B2_D1_Q120_Bot}
        self.running_bots = {}

    def get_all_bots(self):
        return list(self.bots.keys())

    def get_running_bots(self):
        return list(self.running_bots.keys())

    def start_bot(self, pair, bot_name):
        if bot_name in self.get_all_bots():
            bot = self.bots[bot_name](pair)
            if bot.start():
                self.running_bots.update({pair+bot_name:bot})
                return True
        return False
    
    def stop_bot(self, pair, bot_name):
        if pair+bot_name in self.get_running_bots():
            if self.running_bots[pair+bot_name].stop():
                self.running_bots.pop(pair+bot_name)
                return True
        return False

    def get_running_bot_info(self, pair, bot_name):
        if pair+bot_name in self.get_running_bots():
            return self.running_bots[pair+bot_name].log()
        return False
