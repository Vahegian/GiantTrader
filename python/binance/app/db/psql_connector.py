# import sqlalchemy as db
import psycopg2 as p2

class PSQLConnector:
    def __init__(self):
        self._engine = None
        self._cur = None

    def check_engine(func):
        def inner(self, *args, **kwargs):
            if self._engine==None or self._cur==None:
                print(f"\nError on call '{func.__name__}' \nPlease initialize 'postgres' db, use 'Connector.connect(db, user, password, host, port)' !!!")
                return
            else:
                return func(self, *args, **kwargs)
        return inner

    def connect(self, db, user, password, host="docker_db_1", port="5432"):
        try:
            self._engine = p2.connect(database = db, user = user, password = password, host = host, port = port)
            self._cur = self._engine.cursor()
        except Exception as e:
            print(str(e))
    
    @check_engine
    def create_table(self, tname, cols):
        self.execute(f'''CREATE TABLE {tname}
                    ({cols});''')
    
    @check_engine
    def drop_table(self, tname):
        self.execute(f'''DROP TABLE {tname};''')
        
    @check_engine
    def insert_into_table(self, tname, cols, rows):
        self.execute(f'''INSERT INTO {tname}
                    ({cols})
                    VALUES
                    {rows};''')

    @check_engine
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
        
    @check_engine
    def update_table(self, tname, col, conds=None):
        options = [f"UPDATE {tname}", f"SET {col}" ,f"WHERE {conds}"]
        qString = ""

        if tname==None or col==None:
            return
        else:
            qString+=options[0]+" "+options[1]

        if conds != None:
            qString+=" "+options[2]+";"
        else:
            qString+=";"
        self.execute(qString)

    @check_engine
    def delete_from(self, tname, conds):
        options = [f"DELETE ", f"FROM {tname}" ,f"WHERE {conds}"]
        qString = ""

        if tname==None or conds==None:
            return
        else:
            qString+=options[0]+" "+options[1]+" "+options[2]+";"
        self.execute(qString)
        
    @check_engine
    def execute(self, command):
        self._cur.execute(command)
        self._engine.commit()
        print(f"{command} OK.")

    @check_engine
    def disconnect(self):
        self._engine.close()
        self._engine = None
        self._cur = None
   

if __name__ == "__main__":
    c = Connector()
    # c.connect('postgres://myuser@docker_db_1:5432/gtbinance')
    c.connect("gtbinance","myuser","pass")
    # c.drop_table("users")
    c.create_table("users", '''id INT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                enc_pass CHAR(128), 
                                apikey CHAR(128),
                                secret CHAR(128)''')
    c.insert_into_table("users", "id, name, enc_pass", '''(1, 'vahe', '9234708uj')''')
    c.insert_into_table("users", "id, name, enc_pass", '''(2, 'avahe', '9234708uj')''')
    print(c.select_from("users", "*", "enc_pass>'92'", "name", dec=True, limit=1))
    c.update_table("users", "name='ang'", "id='1'")
    print(c.select_from("users", "*"))
    c.delete_from("users", "id='2'")
    print(c.select_from("users", "*"))
    c.drop_table("users")
    c.disconnect()
    