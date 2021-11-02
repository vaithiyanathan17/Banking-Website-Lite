import sqlite3
class testData:
    def __init__(self,**kwargs):
        self.name = kwargs['Name']
        self.dob = kwargs['dob']
        self.Pass = kwargs['Password']
        self.Email = kwargs['eMail']
        self.phone = kwargs['phone']
        self.addr = kwargs['addr']
        self.username=kwargs['upd']
        self.photo=kwargs['photo']
        self.acc_type=kwargs['acc_type']
        self.deposits=kwargs['deposits']


class data_Base():

    def __init__(self,filename,table_name):
        self.filename=filename
        self.table_name=table_name

    def get_connection(self):
        con = sqlite3.connect(self.filename)
        print("DB CREATED")
        return con

    def create_table(self,con):
        con.execute('''CREATE TABLE IF NOT EXISTS ''' + self.table_name + '''(name,dob,Pass,Email,phone,addr,username,photo,account_type,deposits)''')
        print("Table created")

    def insert_record(self,con,obj):
        qr=f'''INSERT INTO {self.table_name}(name,dob,Pass,Email,phone,addr,username,photo,account_type,deposits) VALUES(?,?,?,?,?,?,?,?,?,?)'''
        con.execute(qr,(obj.name,obj.dob,obj.Pass,obj.Email,obj.phone,obj.addr,obj.username,obj.photo,obj.acc_type,obj.deposits))
        con.commit()
        print("record inserted")

    def update(self, con,clientId,obj):
        c = con.cursor()
        print(clientId)
        print(obj.name)
        c.execute(f'''UPDATE {self.table_name} SET name="{obj.name}",dob="{obj.dob}",Email="{obj.Email}",phone="{obj.phone}",addr="{obj.addr}" WHERE username="{clientId}"''')
        con.commit()
        print('updated')



    def close_con(self,con):
        con.close()
        print("con closed")

