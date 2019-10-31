from db.connector import Connector
from contextlib import contextmanager

class DBManager:
    def __init__(self, db_name, user, password, host, port='5432'):
        self._db_name = db_name
        self._user = user
        self._pass = password
        self._host = host
        self._port = '5432'
        self._connector = Connector()

    @contextmanager
    def postgdb(self):
        try:
            self._connector.connect(self._db_name, self._user, self._pass,
                                self._host, self._port)
        
            yield self._connector
        except Exception as e:
            print(str(e))
        finally:
            self._connector.disconnect()

    def create_table(self, tname, col_names, col_types):
        if len(col_names)==len(col_types)>0:
            columns = ""
            for citem, vitem in zip(col_names, col_types):
                columns+=citem+" "+vitem+","
            columns = columns[:-1]
            # print(columns)
            with self.postgdb() as db:
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
            with self.postgdb() as db:
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
        with self.postgdb() as db:
            return db.select_from(tname,colums,conds, order_col, dec, limit)

    def update_table(self, tname, cols_array, values_array, cond=None):
        if len(cols_array)==len(values_array)>0:
            cols = ""
            for ci, vi in zip(cols_array, values_array):
                cols += ci+"="+vi+"," 
            cols = cols[:-1]

            with self.postgdb() as db:
                db.update_table(tname, cols, cond)

    def delete_from_table(self, tname, cond):
        with self.postgdb() as db:
            db.delete_from(tname, cond)

    def drop_table(self, tname):
        with self.postgdb() as db:
            db.drop_table(tname)

if __name__ == "__main__":
    dbm = DBManager("gtbinance","myuser","pass", "docker_db_1")
    with dbm.postgdb() as db:
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
