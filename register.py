import os
import urllib

import jinja2
import webapp2


import urllib

from google.appengine.ext import ndb
from everyThingModel import EvUsers






JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class LoginPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'html/xml'
        template = JINJA_ENVIRONMENT.get_template('login.html')
        template_values = {'errormsg': ''}
        self.response.write(template.render(template_values))    



class RegisterPage(webapp2.RequestHandler):

    def get(self):
        #self.response.headers['Content-Type'] = 'html/xml'
        template = JINJA_ENVIRONMENT.get_template('register.html')
        template_values = {'errormsg': ''}
        self.response.write(template.render(template_values))


class ProcessSigninPage(webapp2.RequestHandler):

    def post(self):
        userinfo = self.request.get("username")   
        passwd = self.request.get("pass")  
        
        curUser = EvUsers.query(ndb.AND(EvUsers.username==userinfo,EvUsers.password==passwd)).get()
        
        if (curUser):
        	self.response.status = 200
        	return self.response
        else:
        	print "error get user: " + userinfo 
        	self.response.status = 404
        	return self.response
          	


class MainPage(webapp2.RequestHandler):

    def post(self):
        userinfo = self.request.get("username")   
        passwd = self.request.get("pass")
        repassword = self.request.get("repass")
        template = JINJA_ENVIRONMENT.get_template('register.html')
        print "email :  " + userinfo
        print "password :" + str(len(passwd))
        print "repassword :" + str(cmp(str(passwd),str(repassword)))
        if (0 != cmp(str(passwd),str(repassword))):
          #self.response.status = 200
          self.response.status_message = "Password and confirm password are not consistent"
          
          template_values = {'errormsg': 'Password and confirm password are not consistent'}
          self.response.write(template.render(template_values))
          print "error1"
        else :  
          #q = db.Query(EvUsers).filter('username =', userinfo)
          print "check user :" +   userinfo
          user_old = EvUsers.query(EvUsers.username == userinfo).get()
          #user_old = Users.get_or_insert(userinfo) 
          if user_old:
        		template_values = {'errormsg': 'user is already exists'}
        		self.response.write(template.render(template_values))  
        		print "error2"        		      			
          else : 	
            #user = Users(key_name=userinfo,username=userinfo,password=passwd)
            #user.put() 
            user_old = EvUsers(username=userinfo,password=passwd)
            #user_old.username =  userinfo
            #user_old.password = passwd
            #user_old.temp = 100
            user_old.put()
            #self.response.headers['Content-Type'] = 'text/plain'
            #q = db.Query(Users).filter('username =', userinfo)
            user_old1 = EvUsers.query(EvUsers.username == userinfo).get()
            #user_old1.password
            #self.response.write("Hello, register module!, User : " + username + " Pass : " + password)
            template = JINJA_ENVIRONMENT.get_template('suc.html')
            template_values = {'greetings': 'greetings'}
            self.response.write(template.render(template_values))
          


application = webapp2.WSGIApplication([
    ('/register/index', RegisterPage),
    ('/register/submit', MainPage),
    ('/register/login', LoginPage),
    ('/register/signin', ProcessSigninPage),
], debug=True)
