from flask import request
class testData:
    def __init__(self,**kwargs):
        self.name = kwargs['Name']
        self.dob = kwargs['dob']
        self.Pass = kwargs['Password']
        self.Email = kwargs['eMail']
        self.phone = kwargs['phone']
        self.addr = kwargs['addr']
        self.username=kwargs['upd']

