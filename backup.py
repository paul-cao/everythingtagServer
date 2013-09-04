import webapp2


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, backup module!')


application = webapp2.WSGIApplication([
    ('/backup/', MainPage),
], debug=True)
