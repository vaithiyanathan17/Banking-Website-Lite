import sqlite3
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt()

class editData:
    def __init__(self,**kwargs):
        self.name = kwargs['Name']
        self.dob = kwargs['dob']
        self.Email = kwargs['eMail']
        self.phone = kwargs['phone']
        self.addr = kwargs['addr']


class fetch():
    def __init__(self,filename,tablename):
        self.filename=filename
        self.tablename=tablename
    def connection(self):
        conn = sqlite3.connect(self.filename)
        return conn

    def select_all(self,conn,client,sec):
        c=conn.cursor()
        easy=c.execute(f"SELECT username,Pass FROM {self.tablename} where username='{client}'")
        save=[]
        for i in easy:
            save.append(i[0])
            save.append(i[1])
        decrypted = bcrypt.check_password_hash(save[1], sec)
        if client == save[0] and decrypted==True:
            return True
        else:
            return False

    def type(self,conn,client):
        c=conn.cursor()
        c.execute(f"SELECT account_type FROM {self.tablename} WHERE username='{client}'")
        items = c.fetchall()
        return items

    def fetch_one(self,conn,client):
        c=conn.cursor()
        c.execute(f"SELECT * FROM {self.tablename} WHERE username='{client}'")
        all_item = c.fetchall()
        return all_item


    def fetch_all(self,conn):
        c=conn.cursor()
        c.execute(f"SELECT * FROM {self.tablename}")
        all_item = c.fetchall()
        return all_item





    def conn_close(self,conn):
        conn.close()
        print('closed')