import sqlite3
import re  # Used for SQL sanitization

'''
This SQL Manager file is designed to control many different SQL tables. Each correspond to 1 Python class (let's call each X).
I will design it so that each X.py imports this SQL Manager, not the other way around. To prevent circular import and make the design modular.
Thus, this file will only have non table specific functions, besides functions to create tables.
'''

class SQLite_Manager:
    def __init__(self):
        self.conn = sqlite3.connect('Backend/DB/Users.db')
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
    
    def isEnglishORNum(s):
        return bool(re.fullmatch(r'[A-Za-z0-9]+', s))
    
    
    def insertARow(self, tableName: str, *args):
        try:
            # Sanitize all
            if not SQLite_Manager.isEnglishORNum(tableName):
                return False
            
            placeholders = ', '.join(['?'] * len(args))
            command = f"INSERT INTO {tableName} VALUES ({placeholders})"
            self.cursor.execute(command, args)
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    
    def getRow(self, tableName: str, column: str, value: str):
        try:
            # Sanizie all
            if not SQLite_Manager.isEnglishORNum(tableName) or not SQLite_Manager.isEnglishORNum(column) or not SQLite_Manager.isEnglishORNum(value):
                return False

            query = f"SELECT * FROM {tableName} WHERE {column} = ?"
            self.cursor.execute(query, (value,))
            results = self.cursor.fetchall()

            if len(results) == 0:
                return False

            # DEBUG
            for x in results:
                print(x)
            return True
        except Exception as e:
            return False
    
    def getAllRows(self, tableName: str):
        try:
            # Sanizie tableName, column, and value
            if not SQLite_Manager.isEnglishORNum(tableName):
                return False

            query = f"SELECT * FROM {tableName}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if len(results) == 0:
                return False

            # DEBUG
            for x in results:
                print(x)
            return True
        except Exception as e:
            return False
    

