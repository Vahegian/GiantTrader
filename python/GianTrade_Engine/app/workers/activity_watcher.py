import datetime
from contextlib import contextmanager

class ActivityWatch:
    def __init__(self, db):
        self.TAG = "ActivityWatch"
        self.ACTIVITY_MONITOR_TABLE_NAME = "amtable"
        self.ACTIVITY_TABLE_COLS = ["id", "date", "uname", "action", "pair", "amount", "price", "fee"]
        self.ACTIVITY_TABLE_COL_TYPES = ["INT PRIMARY KEY NOT NULL", "TEXT NOT NULL", 
                                        "TEXT NOT NULL", "TEXT NOT NULL", "TEXT NOT NULL", 
                                        "TEXT NOT NULL", "TEXT NOT NULL", "TEXT NOT NULL"]
        self.__db = db
        self.__create_table()
        self.__Uid = 0

    def update_Uid(self):
        if self.__Uid>0:
            self.__Uid+=1
        else:
            self.__Uid = self.__get_last_Uid()+1
        

    def __get_last_Uid(self):
        data = self.__db.select_from_table(self.USER_TABLE_NAME, ["*"])
        try:
            if len(data)>0:
                uid = data[-1][0]
                print(uid)
                if int(uid)>0:
                    return int(uid)
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            print(str(e))

    def __create_table(self):
        try:
            self.__db.create_table(self.ACTIVITY_MONITOR_TABLE_NAME, self.ACTIVITY_TABLE_COLS, 
                                    self.ACTIVITY_TABLE_COL_TYPES)   
        except Exception as e:
            print(str(e))

    def __drop_table(self):
        self.__db.drop_table(self.ACTIVITY_MONITOR_TABLE_NAME) 
    
    @contextmanager
    def record(self):
        tdict = {"uname":None, "action":None, "pair":None, 
                 "amount":None, "price":None, "fee":None}
        
        yield tdict
    
        if None in list(tdict.values()):
            raise ValueError(f"{self.TAG} 'None' value was supplied to record")
        else:
            self.update_Uid()
            data = [f'{self.__Uid}', f'"{str(datetime.datetime.now())}"', f'"{tdict["uname"]}"',
                    f'"{tdict["action"]}"', f'"{tdict["pair"]}"', f'"{tdict["amount"]}"',
                    f'"{tdict["price"]}"', f'"{tdict["fee"]}"']
            print(data)
            self.__db.insert_to_table(self.ACTIVITY_MONITOR_TABLE_NAME, self.ACTIVITY_TABLE_COLS, data)
   