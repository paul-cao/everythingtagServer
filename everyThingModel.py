from google.appengine.ext import ndb
import datetime
import re

USERNAME = "username"
PASSWORD = "pass"
CONFIRMPASS = "repass"

GLOBAL_USER_ID = 0
GLOBAL_DEV_ID = 0
GLOBAL_PATH_ID = 0


#User table error code and information

USERS_SUCCESS = 0
USERS_NAMELENERR = 1                  #username is too short
USERS_DUPLICATEERR = 2                #user is exists
USERS_LETTERERR = 3                   #username include invalid letter  
USERS_PASSLENERR = 4                  #password is too short   
USERS_PASSMATCHERR = 5                #passwd and confirm passwd are not match

#EvScannerDev table
ScannerDev_DEVTYPE_BLUETOOTH = 0
ScannerDev_DEVTYPE_BLUETOOTHLOWENERGY = 1




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
	
	#surport function
	#def removeUser(username)
	#def createOrModifyUser(self)
	#def getUser(usName) static
	#def isUserValid(usName,passwd) static
	#def isUserExists(usName) static
	#def isUsernameValid(self,usName)
	#def isPasswordValid(self,passwd,repasswd)
	#def updateUser(self,newTime)
	#def removeUser(username)
	
	
	#Caller is responsible for init the value of attributes 
	@ndb.transactional
	def createOrModifyUser(self):
		global GLOBAL_USER_ID
		self.userid = GLOBAL_USER_ID + 1
		GLOBAL_USER_ID += 1
		self.updateUser(datetime.datetime.now())
		self.put()

	@staticmethod
	def getUser(usName):
		return query(ndb.AND(EvUsers.username==usName,EvUsers.password==passwd)).get()

	@staticmethod
	def isUserValid(usName,passwd):
		user_old = query(ndb.AND(EvUsers.username==usName,EvUsers.password==passwd)).get()
		if (user_old):
			return True
		else:
			return False
		
	@staticmethod
	def isUserExists(usName):
		user_old = EvUsers.query(EvUsers.username == usName).get()
		if (user_old):
			return True
		else:
			return False
		
	def isUsernameValid(self,usName):
		if ((None == usName) or (len(usName) < 5)):	
			return USERS_NAMELENERR				
   	   

		user_old = EvUsers.isUserExists(usName)		  	
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
  	
  	
  @ndb.transactional	
	def updateUser(self,newTime):
		self.updateTime = newTime
		self.put()
	

	@staticmethod
	@ndb.transactional	
	def removeUser(username):  
		isExists = EvUsers.isUserExists(username) 	
		if (False == isExists):
			return
		
		userInfo = EvUser.getUser(username)
		if (None == userInfo):
			return
		
		userInfo.delete()	


################################   EvScanDevHistory  ###############################################



class EvScanDevHistory(ndb.Model):  
  devType = ndb.IntegerProperty()	
  macInfo = ndb.StringProperty()  
  createDate = ndb.DateTimeProperty(auto_now_add=False)  
  deleteDate = ndb.DateTimeProperty(auto_now_add=False)  
  logicType = ndb.IntegerProperty()  
  userID = ndb.IntegerProperty() 
  
  @staticmethod
  def registerDevHistory(device):
  	if (None == device):
  		return
  	history = EvScanDevHistory()
  	history.devType = device.devType
  	history.macInfo = device.macInfo
  	history.createDate = device.createDate
  	history.logicType = device.logicType
  	history.userID = devices.createUserID
  	history.deleteDate = datetime.datetime.now()
  	history.put()



################################   EvDevPath  ###############################################  	

class EvDevPath(ndb.Model):
	deviceID = ndb.IntegerProperty()	
#  devType = ndb.StringProperty()	  
#  macInfo = ndb.StringProperty()	
  updateDate = ndb.DateTimeProperty(auto_now_add=True)  
  placeOccurency = ndb.GeoPtProperty()
  userID = ndb.IntegerProperty()		

  #caller need to init attributes of object
  @staticmethod
  def addDevPathInfo(oldInfo):
  	if (None == oldInfo):
  		return
  		
  	newPath = EvDevPath()
  	newPath.deviceid = oldInfo.deviceID
  	newPath.updateDate = oldInfo.lastUpdateDate
  	newPath.placeOccurency = oldInfo.lastPlace
  	newPath.userID = oldInfo.reportUserID
  	newPath.put()
  	
  @staticmethod 
  def deleteDevPaths(devid):
  	all_path = EvDevPath.query((EvDevPath.deviceID==devid))
  	
  	for path in all_path:
  		path.delete()
  		
  		
################################   EvScannerDev  ###############################################  	
	
class EvScannerDev(ndb.Model):	
  deviceID = ndb.IntegerProperty()  
  devType = ndb.IntegerProperty()
  macInfo = ndb.StringProperty()
  createDate = ndb.DateTimeProperty(auto_now_add=True)
  lastUpdateDate = ndb.DateTimeProperty(auto_now_add=False)
  lastPlace = ndb.GeoPtProperty()
  reportUserID = ndb.IntegerProperty()
  logicType = ndb.IntegerProperty()  
  createUserID = ndb.IntegerProperty()    


  #def createScanDevice(self)
  #def isDeviceExists(devtype,macinfo)
  #def getScanDevice(devtype,macinfo)
  #def updateScanDevice(self)
  #def deleteScanDevice(self,devtype,macinfo)
  
  
  #caller need init attributes before call this function
  @ndb.transactional
	def createScanDevice(self): 
		global GLOBAL_DEV_ID
		self.deviceID = GLOBAL_DEV_ID + 1
		GLOBAL_DEV_ID += 1
		self.createDate = datetime.datetime.now()
		self.put()
  
	@staticmethod  
	def isDeviceExists(devtype,macinfo): 
		curDev = EvScannerDev.query(ndb.AND(EvScannerDev.devType==devType,EvScannerDev.macInfo==macInfo)).get()
		if (curDev):
			return True
		else:
			return False


	@staticmethod  
	def getScanDevice(devtype,macinfo): 
		return EvScannerDev.query(ndb.AND(EvScannerDev.devType==devType,EvScannerDev.macInfo==macInfo)).get()

  #caller need init attributes before call this function
  @ndb.transactional
	def updateScanDevice(self,userinfo): 

		#add a record into Path kind
		EvDevPath.addDevPathInfo(self)

    #update info
		self.lastUpdateDate = datetime.datetime.now()
		self.createDate = datetime.datetime.now()
		self.reportUserID = userinfo.userid
		self.put()


  #caller need init attributes before call this function
  @staticmethod
  @ndb.transactional
	def deleteScanDevice(devtype,macinfo): 
		if ((None == devtype) or (None == macinfo)):
			return
			
		devIsExists = EvScannerDev.isDeviceExists(devtype,macinfo)
		if (False == devIsExists):
			return 
		
		devInfo = EvScannerDev.getScanDevice(devtype,macinfo)
		if (None == devInfo):
			return
		
		#Delete all of DevPath
		EvDevPath.deleteDevPaths(devInfo.deviceID)
		
		#add a record into History kind
		EvDevHistory().registerDevHistory(devInfo) 
		self.delete()


