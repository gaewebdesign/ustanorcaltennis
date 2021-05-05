import webapp2  # (NEWSESSION)

import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

import urllib
import re
import datetime
import types

from google.appengine.api import users
import datastore,library

#from appengine_utilities.sessions import Session
import mysession # (NEWSESSION)

class Author(object):

  def  __init__(self,fname,lname):
    self.author = fname + " " + lname


class Court:
   weekday=""            # day of week
   date=""               # date of reservation

   captain=""            # 
   team=""               # 

   courts=""             # courts (string)
   start=""              # start time   (converted to am/pm)
   end=""                # end time     (converted to am/pm)
   desc=""               # description  

class Template(   mysession.BaseHandler):

    def get(self):

#       guestbook_name=self.request.get('guestbook_name')
#        greetings_query = Greeting.all().ancestor(
#            guestbook_key(guestbook_name)).order('-date')
#        greetings = greetings_query.fetch(10)

#       greetings = ["author":"Joe","Jack","Stacia"]
        a = Author("Ernest" , "Hemingway")
        b = Author("Mark" , "Twain")
        c = Author("John" , "Steinbeck")

        greetings = ["Joe","Jack","Stacia"]
        greetings = [ a,b,c]

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class TestHandler( mysession.BaseHandler):
    def Writeln(self,t):
       self.Write(t)
       self.Write("\n")

    def Write(self,t ):
       self.response.out.write( t )

    def get0(self):

        self.response.headers['Content-Type'] = 'text/html'

        self.Writeln('<html>\n')
        self.Writeln('<head>\n')
        self.Writeln('</head>\n')
        self.Writeln('Testing\n')

        sess = Session()
        if( sess.get(keyname='user') ):
          fname = sess['fname'] 
          lname = sess['lname'] 
          keyname = sess['keyname'] 

          self.Writeln( fname + " " + lname )
          self.Writeln( keyname )

          query="select __key__ from Captain order by lname"
          keys =  db.GqlQuery( query)
          captains = db.get(keys)

          user = datastore.Captain.get_by_key_name( keyname )
          user.count = user.count+10
          db.put( user )

          self.Writeln(  "<br>" )
          for e in captains:
#          self.Writeln( e.fname + " " + e.lname + " " + e.key().name()  + "<br>" )
           g = datastore.Captain.get_by_key_name( e.key().name() )
           self.Writeln( str(g.count) + ") " + g.fname + " " + g.lname + " " + g.key().name()  + "<br>" )
           g.count = g.count+1
           db.put(g)

    def get1(self):

          query="select __key__ from CourtTime order by date"
          keys =  db.GqlQuery( query)
          courtlist=[]
          for k in keys:
             r = db.get(k)
             if( type(r.owner) is not types.NoneType):
                c = Court()
                c.weekday = r.weekday
                c.date = library.cday(r.date)
                c.start = library.ctime(r.start)
                c.end = library.ctime(r.end)
                c.courts = library.listconv(r.courts)
                g = datastore.Captain.get_by_key_name( r.owner )
                c.captain = g.fname + " " + g.lname
                c.team = g.team

                courtlist.append( c)


          for t in courtlist:
                self.Writeln( t.date + " " + t.weekday + " " + t.start + "->" + t.end )
                self.Writeln( t.captain + " " + t.team )
                self.Writeln( "<br>" )
 
    def get3(self):

        url = os.environ["SERVER_NAME"]
        for e in os.environ:
           self.Writeln(e + " " + os.environ[e] + "<br>")

        url = "http://"+os.environ["SERVER_NAME"] + "/" + os.environ["PATH_INFO"]
        self.Writeln(url  + "<br>")
#       if (re.search("localhost",url )): url = "http://localhost:8080"


    def get4(self):


        self.Writeln( " get "  )
        try:
            p = datastore.OpenDate.get_by_key_name( "key_opendate2" )
            if not p:
              self.Writeln( "cant find < ------- " )
        except:
            self.Writeln( "  nope" )
            return


        if( type(p) is types.NoneType):
         opendate = None
         opentime = None
        else:
         opendate = p.openingdate
         opentime = library.ctime(p.openingdate)


    def get(self):
          self.Writeln("testing ")

          query="select __key__ from FacilityRoster"
          keys =  db.GqlQuery( query)
          klist = db.get(keys)
          for e in klist:
             self.Writeln( "delete" + "<br>")
             db.delete(e)

          return

          query="select __key__ from FacilityTeam"
          self.Writeln( query + "<br>")

          keys =  db.GqlQuery( query)
          klist = db.get(keys)
          for e in klist:
             self.Writeln( "delete" + "<br>")
             db.delete(e)



app = webapp2.WSGIApplication(
             [ ('/test', TestHandler )
          ], debug=True , config=mysession.config)



