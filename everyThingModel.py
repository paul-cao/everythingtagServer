from google.appengine.ext import ndb
import datetime
import re

USERNAME = "username"
PASSWORD = "pass"
CONFIRMPASS = "repass"

GLOBAL_USER_ID = 0


#User table error code and information

USERS_SUCCESS = 0
USERS_NAMELENERR = 1                  #username is too short
USERS_DUPLICATEERR = 2                #user is exists
USERS_LETTERERR = 3                   #username include invalid letter  
USERS_PASSLENERR = 4                  #password is too short   
USERS_PASSMATCHERR = 5                #passwd and confirm passwd are not match



USERS_ERRINFO = [
"User is correct",
"The length of username must be large or equal to 5",
"User is exists already",
"Username can be alphabit, digit and underscore only, and must begin with alphabit",
"The length of password must be large or equal to 6",
"The password and confirm password are not match"
]

class EvUsers(ndb.Model):
	username = ndb.StringProperty()
	password = ndb.StringProperty();
	createDate = ndb.DateTimeProperty(auto_now_add=True)
	updtateTime = ndb.DateTimeProperty(auto_now_add=False)
	userid = ndb.IntegerProperty()
	
	#Caller is responsible for init the value of attributes 
	def createOrModifyUser(self):
		global GLOBAL_USER_ID
		self.userid = GLOBAL_USER_ID + 1
		GLOBAL_USER_ID += 1
		self.updateUser(datetime.datetime.now())
		self.put()
		
	
	def isUserExists(self,usName):
		user_old = EvUsers.query(EvUsers.username == usName).get()
		if (user_old):
			return True
		else:
			return False
		
	def isUsernameValid(self,usName):
		if ((None == usName) or (len(usName) < 5)):	
			return USERS_NAMELENERR				
   	   

		user_old = self.isUserExists(usName)		  	
		if (user_old == True):   
     #user is exists
			return USERS_DUPLICATEERR   	   
     
		regular = re.match(r"^[A-Za-z][A-Za-z0-9_]*$",usName)   	
		if (None == regular): 				
			return USERS_LETTERERR   	       	
    	
		return USERS_SUCCESS	   
   
   
	def isPasswordValid(self,passwd,repasswd):  
		if (passwd == None) or (len(passwd) < 6): 	  		
			return USERS_PASSLENERR   		
  	
  	
		if (0 != cmp(str(passwd),str(repasswd))):   		
			return USERS_PASSMATCHERR   		
  		
		return USERS_SUCCESS	
  	
  	
  	
	def updateUser(self,newTime):
		self.updateTime = newTime
		self.put()
	
	
	
class EvScannerDev(ndb.Model):	
  devType = ndb.StringProperty()
  macInfo = ndb.StringProperty()
  createDate = ndb.DateTimeProperty(auto_now_add=True)
  lastUpdateDate = ndb.DateTimeProperty(auto_now_add=False)
  lastPlace = ndb.GeoPtProperty()
  
	
	