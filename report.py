import webapp2

import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation

from everyThingModel import EvScannerDev

from google.appengine.ext import ndb

import datetime

def getText(nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

class MainPage(webapp2.RequestHandler):


    
    def post(self):
        ''' 
        
        
        
        '''
        print "body = " + str(self.request.body)
        doc = xml.dom.minidom.parseString(self.request.body)
        
        top = doc.getElementsByTagName("devices")
        
        devices = top[0].getElementsByTagName("device")
        
        for device in devices:
        	print "get device"
        	eleDevType = device.getElementsByTagName("devtype")
        	eleMacInfo = device.getElementsByTagName("macinfo")
        	eleGeo = device.getElementsByTagName("geoinfo")
        	devType = getText(eleDevType[0].childNodes)
        	macInfo = getText(eleMacInfo[0].childNodes)
        	geoInfo = getText(eleGeo[0].childNodes)
        	
        	print "get devType = " + devType
        	print "get macInfo = " + macInfo
        	print "get geoInfo = " + geoInfo
        	lan_str,log_str = geoInfo.split(',')
        	lan = float(lan_str)
        	log = float(log_str)
        	print "lan = " + str(lan)
        	print "log = " + str(log)
        	
        	curDev = EvScannerDev.query(ndb.AND(EvScannerDev.devType==devType,EvScannerDev.macInfo==macInfo)).get()
        	if curDev:
        		curDev.lastUpdateDate = datetime.datetime.now()
        		curDev.lastPlace = ndb.GeoPt(lan, log)
        		curDev.put()
        		self.response.status = 200
        		return self.response
        	else:
        		self.response.status = 404
        		return self.response
        
        #userinfo = self.request.get("username")
        #passwd = self.request.get("pass")
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, report module!')
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, report module!')
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('Hello, report module!')


application = webapp2.WSGIApplication([
    ('/report/', MainPage),
], debug=True)
