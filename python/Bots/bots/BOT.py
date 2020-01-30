class BOT:
    def __init__(self):
        self.__log = []
        self.__log_id = 0
    def start(self):
        return False
    def stop(self):
        return False
    def add_log(self, data):
        if len(self.__log) > 200:
            self.__log.pop(0)
        self.__log_id+=1
        self.__log.append([self.__log_id, data])
    def get_log(self):
        return self.__log
    def get_bot_info(self):
        return ["not implemented"]