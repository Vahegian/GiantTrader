
class UserManager:
    def __init__(self, db):
        self.USER_TABLE_NAME = "utable"
        self.USER_TABLE_COLS = ["id", "name", "pass", "apiKey", "secret"]
        self.USER_TABLE_COL_TYPES = ["INT PRIMARY KEY NOT NULL", "TEXT NOT NULL", 
                                        "TEXT NOT NULL", "TEXT NOT NULL", "TEXT NOT NULL"]
        self.__db = db
        self.__create_user_table()
        self.__Uid = 0

    def update_Uid(func):
        def inner(self, *args, **kwargs):
            if self.__Uid>0:
                self.__Uid+=1
            else:
                self.__Uid = self.__get_last_Uid()+1
            return func(self, *args, **kwargs)
        return inner

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

    def __create_user_table(self):
        try:
            self.__db.create_table(self.USER_TABLE_NAME, self.USER_TABLE_COLS, 
                                    self.USER_TABLE_COL_TYPES)   
        except Exception as e:
            print(str(e)) 

    @update_Uid
    def add_user(self, name, password, apikey, apisecret):
        self.__db.insert_to_table(self.USER_TABLE_NAME, self.USER_TABLE_COLS, [f'{self.__Uid}', 
                                    f"'{name}'", f"'{password}'",f"'{apikey}'", f"'{apisecret}'"])

    def get_user_info(self, uname, password):
        return self.__db.select_from_table(self.USER_TABLE_NAME, ["*"], 
                                [f"{self.USER_TABLE_COLS[1]}='{uname}'",
                                 f"{self.USER_TABLE_COLS[2]}='{password}'"])[0]

    def test_run(self):
        self.__db.create_table(self.USER_TABLE_NAME, self.USER_TABLE_COLS, self.USER_TABLE_COL_TYPES)
        self.__db.insert_to_table(self.USER_TABLE_NAME, self.USER_TABLE_COLS, ['1', "'vahe'", "'pass'","'api'", "'sec'"])                
        self.__db.insert_to_table(self.USER_TABLE_NAME, self.USER_TABLE_COLS, ['2', "'vahe'", "'pass'","'api'", "'sec'"])
        print(self.__db.select_from_table(self.USER_TABLE_NAME, ["*"]))
        self.__db.update_table(self.USER_TABLE_NAME, ["name"], ["'Kola'"], "id='2'")
        print(self.__db.select_from_table(self.USER_TABLE_NAME, ["*"]))
        self.__db.delete_from_table(self.USER_TABLE_NAME, "id='1'")
        print(self.__db.select_from_table(self.USER_TABLE_NAME, ["*"]))
        self.__db.drop_table(self.USER_TABLE_NAME)