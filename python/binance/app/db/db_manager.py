# from db.psql_connector import PSQLConnector
from db.sql_lite_connector import SQLLConnector
from contextlib import contextmanager

DB_FILE = "./db.db"
class DBManager:
    def __init__(self, db_name=None, user=None, password=None, host=None, port='5432', db_file=None):
        self.__db_name = db_name
        self.__user = user
        self.__pass = password
        self.__host = host
        self.__port = port
        self.__db_file = db_file

    @contextmanager
    def db_cur(self):
        try:
            self.__connector = SQLLConnector()
            if self.__db_file != None:
                self.__connector.connect(self.__db_file)
            else:
                self.__connector.connect(DB_FILE)
        
            yield self.__connector
        except Exception as e:
            print(str(e))
        finally:
            self.__connector.disconnect()

    def create_table(self, tname, col_names, col_types):
        if len(col_names)==len(col_types)>0:
            columns = ""
            for citem, vitem in zip(col_names, col_types):
                columns+=citem+" "+vitem+","
            columns = columns[:-1]
            # print(columns)
            with self.db_cur() as db:
                db.create_table(tname, columns)

    def insert_to_table(self, tname, cols_array, values_array):
        cols = ""
        vals = "("
        if len(cols_array)==len(values_array)>0:
            for citem, vitem in zip(cols_array, values_array):
                cols+=citem+","
                vals+=vitem+","
            cols = cols[:-1]
            vals = vals[:-1]+")"
        # print(cols, "\n", vals)
            with self.db_cur() as db:
                db.insert_into_table(tname, cols, vals)

    def select_from_table(self, tname, cols, conds_array=None, order_col=None, dec=False, limit=None):
        colums = ""
        conds = None
        for item in cols:
            colums+= item+","
        colums = colums[:-1]
        if conds_array!=None:
            conds=""
            for item in conds_array:
                conds+= item+" AND "
            conds = conds[:-5]
        with self.db_cur() as db:
            return db.select_from(tname,colums,conds, order_col, dec, limit)

    def update_table(self, tname, cols_array, values_array, cond=None):
        if len(cols_array)==len(values_array)>0:
            cols = ""
            for ci, vi in zip(cols_array, values_array):
                cols += ci+"="+vi+"," 
            cols = cols[:-1]

            with self.db_cur() as db:
                db.update_table(tname, cols, cond)

    def delete_from_table(self, tname, cond):
        with self.db_cur() as db:
            db.delete_from(tname, cond)

    def drop_table(self, tname):
        with self.db_cur() as db:
            db.drop_table(tname)

if __name__ == "__main__":
    dbm = DBManager("gtbinance","myuser","pass", "docker_db_1")
    with dbm.db_cur() as db:
        db.create_table("users", '''id INT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                enc_pass CHAR(128), 
                                apikey CHAR(128),
                                secret CHAR(128)''')
        db.insert_into_table("users", "id, name, enc_pass", '''(1, 'vahe', '9234708uj')''')
        db.insert_into_table("users", "id, name, enc_pass", '''(2, 'avahe', '9234708uj')''')
        print(db.select_from("users", "*", "enc_pass>'92'", "name", dec=True, limit=1))
        db.update_table("users", "name='ang'", "id='1'")
        print(db.select_from("users", "*"))
        db.delete_from("users", "id='2'")
        print(db.select_from("users", "*"))
        db.drop_table("users")
