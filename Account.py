class User:
    def __init__(self):
        self.LoggedIn = False
        print(1)

    def Login(self,Id,Type):
        self.LoggedIn = True
        self.Id = Id
        self.Type = Type
    def Logout(self):
        self.LoggedIn = False
        self.Id = 0
        self.Type = 0
a = User()
print(a.LoggedIn)
a.Login(1,'a')
print(a.LoggedIn)
a.Logout()
print(a.LoggedIn)

