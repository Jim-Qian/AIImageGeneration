from DB.SQLite_Manager import SQLite_Manager
from DB.User import User

# def createUser(username, password, balance, isAdmin):
#   user1 = User(username, password, balance, isAdmin)
#   user1.insertIntoDB(sqlManager)


sqlManager = SQLite_Manager() 

sqlManager.createUsersTable()
user1 = User("Jim", "AdminJim2025Admin", 100, True)
user1.insertIntoDB(sqlManager)
user2 = User("Guest", "Guest", 0, False)
user2.insertIntoDB(sqlManager)

sqlManager.getAllRows("Users")
pass
