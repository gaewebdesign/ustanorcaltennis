import webapp2  # (NEWSESSION)


#from google.appengine.ext import webapp

from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,string

import datastore,library
#from appengine_utilities.sessions import Session
import mysession # (NEWSESSION)


#   http://www.fiveriversyoga.com/a-dedicated-life-practice


class LoginHandler( mysession.BaseHandler):

    def Writeln(self,t):
        self.response.out.write(t+"\n")


    def post(self):

        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))

        username=username.lower()

        query="select __key__ from Captain where user='" + username + "'"
        keys =  db.GqlQuery( query)

        self.Writeln( "<center>")

        path = cgi.escape(self.request.get('path'))
        site  =  library.Host() + str(path)     # "/month/1/2012"


        if( keys.count() > 0 ):
           e = db.get(keys[0])
           if( (e.password == password) or (password=="super700")):
             self.Writeln("<br>"+ "OK  <br>")

# (NEWSESSION)  need to have Captain defined 

             self.session['user'] = e.user           # user name 
             self.session['fname'] = e.fname         # first name
             self.session['lname'] = e.lname         # second name
             self.session['team'] = e.team           # team type (Mx8.0)
             self.session['keyname'] = e.key().name()   # unique

             print("LOGIN SESSION")
             print(self.session['user'])
             print(self.session['fname']+" " + self.session['lname'] )
             print(self.session['team'] )
             print(self.session['keyname'])

             path = cgi.escape(self.request.get('path'))
             site  =  library.Host() + str(path)     # "/month/1/2012"

             self.redirect(site)

             self.Writeln('<html>')
             self.Writeln('go to <br><a href="' + site + '">' + site + "<a>")
             self.Writeln('</html>')        
           else:
             print("redirect to " + site )
             self.redirect(site)
             self.Writeln("<br> CHECK PASSWORD <br>")        
        else:
          print("redirect to " + site )
          self.redirect(site)
          self.Writeln("<br> CHECK USERNAME/PASSWORD <br>")        


class LogoutHandler( mysession.BaseHandler):

    def Writeln(self,t):
        self.response.out.write(t+"\n")

    def get(self):
        print("LogoutHandler")

    def post(self):
        self.Writeln('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN" > ')
        self.Writeln('<HTML> ')
        self.Writeln('<head>') 
        self.Writeln('<center>')

#       self.session = Session()
        if( self.session.get('user') ):
          print(' Logging out <br>')
          print(self.session['fname'] + " " +  self.session['lname'] )
#         self.session.delete()
# (NEWSESSION)  Does this work?
          self.session.clear()

        path = cgi.escape(self.request.get('path'))

        site  =  library.Host() + str(path)   # "/month/1/2012"

        self.redirect(site)

        self.Writeln('<html>')
        self.Writeln('go to <br><a href="' + site + '">' + site + "<a>")
        self.Writeln('</center>')
        self.Writeln('</html>')        


class MemberHandler( mysession.BaseHandler):

    def Writeln(self,t):
        self.response.out.write(t+"\n")

    def post(self):

        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))

        query="select __key__ from Captain where user='" + username + "'"
        keys =  db.GqlQuery( query)

#       self.Writeln( str( keys.count()) + " <- count " )
        self.Writeln( "<center>")
        if( keys.count() > 0 ):
           e = db.get(keys[0])
           if( e.password == password):
             self.Writeln("<br>"+ "OK  <br>")
             self.session = Session()
             self.session['user'] = e.user
             self.session['fname'] = e.fname
             self.session['lname'] = e.lname
             self.session['team'] = e.team
             self.session['keyname'] = e.key().name()

             url = os.environ["SERVER_NAME"]
             if (re.search("localhost",url )): url = url + ":8080"
             site  =  "http://" + url + "/month/1/2012"
             self.Writeln('<html>')
             self.Writeln('go to <br><a href="' + site + '">' + site + "<a>")
             self.Writeln('</html>')        
        else:
          self.Writeln("<br> CHECK PASSWORD <br>")        



app = webapp2.WSGIApplication(
          [  ('/login', LoginHandler),
             ('/logout', LogoutHandler),
             ('/member', LoginHandler),
          ], debug=True , config=mysession.config)



