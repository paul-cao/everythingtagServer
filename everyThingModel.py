from google.appengine.ext import ndb
import datetime

class EvUsers(ndb.Model):
	username = ndb.StringProperty()
	password = ndb.StringProperty();
	createDate = ndb.DateTimeProperty(auto_now_add=True)
	
class EvScannerDev(ndb.Model):	
  devType = ndb.StringProperty()
  macInfo = ndb.StringProperty()
  createDate = ndb.DateTimeProperty(auto_now_add=True)
  lastUpdateDate = ndb.DateTimeProperty(auto_now_add=False)
  lastPlace = ndb.GeoPtProperty()
	
	