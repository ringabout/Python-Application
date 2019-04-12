import os
import sqlite3
from collections import namedtuple


starter = 'Start.db'
starter_info = namedtuple('info',  'fname name state')
   
class DBManger:
    def __init__(self, name):
        self.name = name
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.name)
        return self.conn
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise
   

def read_db():
    if not os.path.exists(starter):
        
#        conn = sqlite3.connect(starter)
        with DBManger(starter) as conn:
            conn.execute("CREATE TABLE starter(fname, name, state)")
            conn.commit()
#        conn.close()
    with DBManger(starter) as conn:
        for row in conn.execute('SELECT * FROM starter'):
            info = starter_info(*row)
            yield info
        

  
  
    

def remove_db():
    with DBManger(starter) as conn:
        conn.execute('DELETE FROM starter')
        conn.commit()



def save2db(start):
    with DBManger(starter) as conn:
        conn.execute("INSERT INTO starter Values (?,?,?)",
                (start.fname, start.name, start.state))
        conn.commit()
 
    
