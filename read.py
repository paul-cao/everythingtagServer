import webapp2

import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
from google.appengine.ext import ndb

from everyThingModel import EvScannerDev

import datetime

from everyThingModel import EvUsers

class MainPage(webapp2.RequestHandler):

    def get(self):
        userinfo = self.request.get("username")   
        passwd = self.request.get("pass")
        devType = self.request.get("devtype")   
        macInfo = self.request.get("macinfo")
        
        temp = ndb.GeoPt(-1.15, -1.89)
        print "temp = " + str(temp)
        
        curUser = EvUsers.query(ndb.AND(EvUsers.username==userinfo,EvUsers.password==passwd)).get()
        if (curUser):
        	curDev = EvScannerDev.query(ndb.AND(EvScannerDev.devType==devType,EvScannerDev.macInfo==macInfo)).get()
        	print "user right"
        	if curDev:
         	  #build html  
         	  print "device right"
         	  impl = getDOMImplementation()
         	  document = impl.createDocument(None, None, None)
         	  devices = document.createElement("devices") 
         	  device = document.createElement("device") 
         	  updateTime = document.createElement("updateTime")
         	  geoInfo = document.createElement("geoinfo")
         	  
         	  
         	  document.appendChild(devices)
         	  
         	  updateTime.appendChild(document.createTextNode(str(curDev.lastUpdateDate)))
         	  geoInfo.appendChild(document.createTextNode(str(curDev.lastPlace)))
         	  
         	  device.appendChild(updateTime)
         	  device.appendChild(geoInfo)
         	  
         	  devices.appendChild(device)
         	  self.response.headers['Content-Type'] = 'text/plain'
         	  self.response.write(document.toprettyxml())
         	  
        	else:
         	  self.response.status = 404        		
         	  return self.response
        else:
          self.response.status = 404
          return self.response        	  		  

              


application = webapp2.WSGIApplication([
    ('/read/', MainPage),
], debug=True)
