from DB.SQLite_Manager import SQLite_Manager
from DB.User import User

# def createUser(username, password, balance, isAdmin):
#   user1 = User(username, password, balance, isAdmin)
#   user1.insertIntoDB(sqlManager)


sqlManager = SQLite_Manager() 
sqlManager.createUsersTable()
user1 = User("Jim", "AdminJim2025Admin", 100, True)
sqlManager.insertNewUserIntoDB(user1.username, user1.password, user1.balance, user1.isAdmin)

sqlManager.getARowFromTable("Users", "username", "Jim")
pass
