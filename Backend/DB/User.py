
from DB.SQLite_Manager import SQLite_Manager

class User:
    def __init__(self, username, password, balance, isAdmin):
        self.username = username
        self.password = password
        self.balance = balance
        self.isAdmin = isAdmin

    def insertIntoDB(self, sqlManager: SQLite_Manager):
        _isAdmin = True if self.isAdmin else False
        sqlManager.insertARow("Users", 
                              self.username, self.password, self.balance, _isAdmin)
        
    def generateImage(self, prompt):
        self.balance -= 0.05
        pass

    