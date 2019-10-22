# import sqlalchemy as db
import psycopg2 as p2

class Connector:
    def __init__(self):
        self._engine = None
        self._cur = None

    def connect(self, db, user, password, host="docker_db_1", port="5432"):
        self._engine = p2.connect(database = db, user = user, password = password, host = host, port = port)
        self._cur = self._engine.cursor()

    # def create_db(self, dbName):
    #     if self._engine != None:
    #         self._engine.execute(f"create database {dbName}")

    def create_table(self, tname, cols):
        self._cur.execute(f'''CREATE TABLE {tname}
                    ({cols});''')
        self._engine.commit()

    def drop_table(self, tname):
        self._cur.execute(f'''DROP TABLE {tname};''')
        self._engine.commit()

    def insert_into_table(self, tname, cols, rows):
        self._cur.execute(f'''INSERT INTO {tname}
                    ({cols})
                    VALUES
                    {rows};''')
        self._engine.commit()

    def select_from(self, tnames, cols, conds=None, order_col=None, dec=False, limit=None):
        options = [f"SELECT {cols}", f"FROM {tnames}", f"WHERE {conds}", f"ORDER BY {order_col}", "DESC", f"LIMIT {limit}"]
        opList = []
        qString = ""
        if tnames==None or cols==None:
            return
        else:
            qString+=options[0]+" "+options[1]
        
        if conds != None:
            opList.append(2)
        if order_col != None:
            opList.append(3)
        if dec:
            opList.append(4)
        if limit != None:
            opList.append(5)

        for index in opList:
            qString+=" "+options[index]
        qString+=";"
        print(qString)
        
        self._cur.execute(qString)
        return self._cur.fetchall()

    def disconnect(self):
        self._engine.close()
    # def list_dbs(self):
        # if self._engine != None:
            # insp = db.inspect(self._engine)
            # return insp.get_schema_names()


if __name__ == "__main__":
    c = Connector()
    # c.connect('postgres://myuser@docker_db_1:5432/gtbinance')
    c.connect("gtbinance","myuser","pass")
    c.drop_table("users")
    c.create_table("users", '''id INT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                enc_pass CHAR(128), 
                                apikey CHAR(128),
                                secret CHAR(128)''')
    c.insert_into_table("users", "id, name, enc_pass", '''(1, 'vahe', '9234708uj')''')
    c.insert_into_table("users", "id, name, enc_pass", '''(2, 'avahe', '9234708uj')''')
    print(c.select_from("users", "*", "enc_pass>'92'", "name", dec=True, limit=1))
    c.disconnect()
    # c.create_db("gian")
    # print(c.list_dbs())