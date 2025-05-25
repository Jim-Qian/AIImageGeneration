import sqlite3

'''
This SQL Manager file is designed to control many different SQL tables. Each correspond to 1 Python class (let's call each X).
I will design it so that each X.py imports this SQL Manager, not the other way around. To prevent circular import and make the design modular.

TODO:
Create a generic INSERT function:
 - Input: Table name and column values
 - Output: Success or failure
Create a generic SELECT function
 - Input: Table name and key
 - Output: All the column values of that row if found
'''

class SQLite_Manager:
    def __init__(self):
        self.conn = sqlite3.connect('Users.db')
        self.cursor = self.conn.cursor()

    def createUsersTable(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                username TEXT PRIMARY KEY,
                password TEXT,
                balance REAL,
                isAdmin BOOL
            )
        ''')
        self.conn.commit()

    def insertNewUserIntoDB(self, username: str, password: str, balance: float, isAdmin: bool):
        # DEBUG
        # Need to sanitize username and password

        isAdminString = 'True' if isAdmin else 'False'
        self.cursor.execute('''
            INSERT INTO Users (username, password, balance, isAdmin) VALUES (?, ?, ?, ?)
        ''', (username, password, balance, isAdminString))
        self.conn.commit()
    
    # DEBUG
    # def getExistingUserFromDB(username):
    #     username = ""
    #     password = ""
    #     balance = 0
    #     isAdmin = False

    #     newUser = User(username, password, balance, isAdmin)
    #     return newUser
