import httplib
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
import datetime


temp = "-1.15,-1.81"
typedev = "bluetohot"
infomac = "1236"

print "temp = " + str(temp)



conn = httplib.HTTPConnection("localhost",8080)
impl = getDOMImplementation()
document = impl.createDocument(None, None, None)
devices = document.createElement("devices") 
device = document.createElement("device") 
devtype = document.createElement("devtype")
geoInfo = document.createElement("geoinfo")
macInfo = document.createElement("macinfo")


document.appendChild(devices)

devtype.appendChild(document.createTextNode(str(typedev)))
geoInfo.appendChild(document.createTextNode(str(temp)))
macInfo.appendChild(document.createTextNode(str(infomac)))

device.appendChild(devtype)
device.appendChild(geoInfo)
device.appendChild(macInfo)

devices.appendChild(device)


print document.toprettyxml()
conn.request("POST","/report/?username=aaaccc&pass=a",document.toprettyxml())

res = conn.getresponse()

print res.status, res.reason


