
from __future__ import annotations  # For forward references without strings (explicit return type)

from DB.SQLite_Manager import SQLite_Manager
from DB.SQLite_Manager import SQLResponse

class User:
    def __init__(self, username: str, password: str, balance: float):
        self.username = username
        self.password = password
        self.balance = balance
        self.isAdmin = False  # Make this into a separate setter so don't accidentally grant admin. Also will make it simplier to search for all the references for the setter.
    
    # Get from DB ----------------------------------------------------------------------
    def getFromDB(sqlManager: SQLite_Manager, username: str) -> User:
        response = sqlManager.getRow("Users",
                          "username", username)
        if (not response.success):
            return None
        user = User(response.list[0], response.list[1], response.list[2])
        if (response.list[3]):
            user.makeAdmin()
        return user
    
    # Set to DB ----------------------------------------------------------------------
    def insertIntoDB(self, sqlManager: SQLite_Manager):
        response = sqlManager.insertARow("Users", 
                              self.username, self.password, self.balance, self.isAdmin)
        return response.success

    def makeAdmin(self, sqlManager: SQLite_Manager = None):
        if sqlManager != None:
            sqlManager.setRowSingleValue("Users",
                                        "username", self.username, "isAdmin", True)
        self.isAdmin = True

    def changeBalance(self, sqlManager: SQLite_Manager, newBalance: float = None):
        if sqlManager != None:
            sqlManager.setRowSingleValue("Users",
                                         "username", self.username, "balance", newBalance)
        self.balance = newBalance
    
    # Miscellaneous functions ---------------------------------------------------------

    