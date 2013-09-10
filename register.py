import os
import urllib

import jinja2
import webapp2


import urllib

import everyThingModel
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
        userinfo = self.request.get(everyThingModel.USERNAME)   
        passwd = self.request.get(everyThingModel.PASSWORD)  
        
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
        userinfo = self.request.get(everyThingModel.USERNAME)   
        passwd = self.request.get(everyThingModel.PASSWORD)
        repassword = self.request.get(everyThingModel.CONFIRMPASS)
                
        template = JINJA_ENVIRONMENT.get_template('register.html')
        print "email :  " + userinfo
        print "password :" + str(len(passwd))
        print "repassword :" + str(cmp(str(passwd),str(repassword)))
        
        newUser = EvUsers()
        retCode = newUser.isUsernameValid(userinfo)
        if (everyThingModel.USERS_SUCCESS != retCode):
        	#username error
        	template_values = {'errormsg': everyThingModel.USERS_ERRINFO[retCode]}
        	self.response.write(template.render(template_values))
        	return self.response
        	
        retCode = newUser.isPasswordValid(passwd,repassword)
        if (everyThingModel.USERS_SUCCESS != retCode):
        	#password error
        	template_values = {'errormsg': everyThingModel.USERS_ERRINFO[retCode]}
        	self.response.write(template.render(template_values))
        	return self.response
        	
        #user information correct, create new user
        newUser.username = userinfo
        newUser.password = passwd
        newUser.createOrModifyUser() 
        template = JINJA_ENVIRONMENT.get_template('suc.html')
        template_values = {'greetings': 'greetings'}
        self.response.write(template.render(template_values))
               	
        


application = webapp2.WSGIApplication([
    ('/register/index', RegisterPage),
    ('/register/submit', MainPage),
    ('/register/login', LoginPage),
    ('/register/signin', ProcessSigninPage),
], debug=True)
