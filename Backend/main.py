# import DB
# import APIs
# from DB import SQLite_Manager
# import Backend.APIs.OpenAI_Client as OpenAI_Client

from DB.SQLite_Manager import SQLite_Manager
from DB.User import User

def createUser(username, password, balance, isAdmin):
  sqlManager = SQLite_Manager() 
  user1 = User(username, password, balance, isAdmin)
  user1.insertIntoDB(sqlManager)
  pass

sqlManager = None
createUser("Jim", "AdminJim2025Admin", 100, True)
pass
