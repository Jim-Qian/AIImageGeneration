import sqlite3

from DB.User import User

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

    def insertNewUserIntoDB(self, username: str, password: str, balance: float, isAdmin: bool):
        # DEBUG
        # Need to sanitize username and password

        isAdminString = 'True' if isAdmin else 'False'
        self.cursor.execute(f'''
            INSERT INTO Users
            (username, password, balance, isAdmin) VALUES (?, ?, ?, ?)", 
            ('{username}', {password}, {balance}, {isAdminString})
        ''')
    
    # DEBUG
    def getExistingUserFromDB(username):
        username = ""
        password = ""
        balance = 0
        isAdmin = False

        newUser = User(username, password, balance, isAdmin)
        return newUser