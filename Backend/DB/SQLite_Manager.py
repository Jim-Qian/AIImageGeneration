'''
This SQL Manager file is designed to control many different SQL tables. Each correspond to 1 Python class (let's call each X).
I will design it so that each X.py imports this SQL Manager, not the other way around. To prevent circular import and make the design modular.
Thus, this file only has non table specific functions, besides functions to create tables.
'''


import os
import sqlite3
import re  # Used for SQL sanitization


class SQLite_Manager:
    def __init__(self):
        # Using absolute path is error-prone.
        db_path = os.path.join(os.path.dirname(__file__), 'Users.db')
        self.conn = sqlite3.connect(db_path)
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
                return SQLResponse(False)
            
            placeholders = ', '.join(['?'] * len(args))
            command = f"INSERT INTO {tableName} VALUES ({placeholders})"
            self.cursor.execute(command, args)
            self.conn.commit()
            return SQLResponse(True)
        except Exception as e:
            return SQLResponse(False)
    
    
    def getRow(self, tableName: str, column: str, value: str):
        try:
            # Sanizie all
            if not SQLite_Manager.isEnglishORNum(tableName) or not SQLite_Manager.isEnglishORNum(column) or not SQLite_Manager.isEnglishORNum(value):
                return SQLResponse(False)

            query = f"SELECT * FROM {tableName} WHERE {column} = ?"
            self.cursor.execute(query, (value,))
            results = self.cursor.fetchall()

            if len(results) == 0:
                return SQLResponse(False)

            list = []
            for row in results:
                # There is only 1 row.
                for value in row:
                    list.append(value)
            return SQLResponse(True, list)
        except Exception as e:
            return SQLResponse(False)
    
    def getAllRows(self, tableName: str):
        try:
            # Sanizie tableName, column, and value
            if not SQLite_Manager.isEnglishORNum(tableName):
                return SQLResponse(False)

            query = f"SELECT * FROM {tableName}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if len(results) == 0:
                return SQLResponse(False)

            list = []
            for row in results:
                list2 = []
                for value in row:
                    list2.append(value)
                list.append(list2)
            return SQLResponse(True, list)
        except Exception as e:
            return SQLResponse(False)
    
    # Finds the row using column and value. Then sets that row's column2 to be value2. value2 can be str, int, or bool.
    def setRowSingleValue(self, tableName: str, column: str, value: str, column2: str, value2):
        try:
            # Sanitize inputs
            if not SQLite_Manager.isEnglishORNum(tableName) or \
            not SQLite_Manager.isEnglishORNum(column) or \
            not SQLite_Manager.isEnglishORNum(column2) or \
            not SQLite_Manager.isEnglishORNum(value):
                return SQLResponse(False)

            query = f"UPDATE {tableName} SET {column2} = ? WHERE {column} = ?"
            self.cursor.execute(query, (value2, value))
            self.conn.commit()

            if self.cursor.rowcount == 0:
                return SQLResponse(False)

            return SQLResponse(True)
        except Exception as e:
            return SQLResponse(False)
    

class SQLResponse:
    def __init__(self, success: bool, list: list = [], message: str = "None"):
        self.success = success
        self.list = list
        self.message = message