class User:
    def __init__(self):
        self.LoggedIn = False
        self.Contract_Id = ''

    def Login(self,Id,Type,password):
        self.LoggedIn = True
        self.Id = Id
        self.Type = Type
        self.password = password
    def Logout(self):
        self.LoggedIn = False
        self.Id = 0
        self.Type = 0

