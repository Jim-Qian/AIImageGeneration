from DB import User
from DB import SQLite_Manager
import OpenAI_Client

sqlManager = None
def createUser(username, password, balance, isAdmin):
  sqlManager = SQLite_Manager() 
  user1 = User(username, password, balance, isAdmin)
  user1.insertIntoDB(sqlManager)
  pass

createUser("Jim", "AdminJim2025Admin", 100, True)
pass
