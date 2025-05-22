
import SQLite_Manager

class User:
    def __init__(self, username):
        self.username = username
        self.password = ""
        self.balance = 0
        self.isAdmin = False

    def insertIntoDB(self, sqlManager):
        sqlManager.insertNewUserIntoDB(self.username, 
                                        self.password, 
                                        self.balance, 
                                        self.isAdmin)
        
    def generateImage(self, prompt):
        self.balance -= 0.05
        # DEBUG
        pass

    