import webapp2


from google.appengine.ext import ndb
from everyThingModel import EvUsers
from everyThingModel import EvScannerDev
import datetime


class MainPage(webapp2.RequestHandler):

        
    def post(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        userinfo = self.request.get("username")   
        passwd = self.request.get("pass")
        devType = self.request.get("devtype")   
        macInfo = self.request.get("macinfo")
        
        print "userinfo = " + userinfo
        print "pass = " + passwd
        print "devtype = " + devType
        print "macInfo = " + macInfo  
        
        curUser = EvUsers.isUserValid(userinfo,passwd)
        if (True == curUser):
        	print "user right"
        	curDev = EvScannerDev.query(ndb.AND(EvScannerDev.devType==devType,EvScannerDev.macInfo==macInfo)).get()
        	if curDev:
        		#exists
        		print "dev exist"
        		self.response.status = 200
        		return self.response        		
        	else:
        		print "add new dev"
        		newDev = EvScannerDev()        		
        		newDev.macInfo = macInfo
        		newDev.devType = devType
        		newDev.createDate = datetime.datetime.now()
        		newDev.put()
        		self.response.status = 200
        		return self.response
        else:
        	#error user
        	self.response.status = 404
        	return self.response
            	   


application = webapp2.WSGIApplication([
    ('/scanner/', MainPage),
], debug=True)
