'''
For debugging only.
'''

from DB.SQLite_Manager import SQLite_Manager
from DB.User import User
from APIs import OpenAI_Client


def testSQLManager():
    sqlManager = SQLite_Manager() 

    sqlManager.createUsersTable()
    user1 = User("Jim", "AdminJim2025Admin", 100)
    user1.makeAdmin()
    user1.insertIntoDB(sqlManager)
    user2 = User("Guest", "Guest", 0)
    user2.insertIntoDB(sqlManager)

    sqlManager.getAllRows("Users")
    pass

def testOpenAIClient():
    OpenAI_Client.test()
    pass

testOpenAIClient()
pass