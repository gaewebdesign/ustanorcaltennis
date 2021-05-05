import webapp2 # (NEWSESSION)

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types

import datastore,library
#from appengine_utilities.sessions import Session

import mysession # (NEWSESSION)



class Reservation:
   fname=""              # Captain name
   lname=""              # Captain name
   team=""               # team
   count=0               # count
   courts=[]             # court list 


class Court:
   weekday=""            # day of week
   date=""               # date of reservation

   courts=""             # courts (string)
   location=""           # LP or Mango
   start=""              # start time   (converted to am/pm)
   end=""                # end time     (converted to am/pm)
   desc=""               # description  

class Captain:
   fname = lname = team = user = ""

class PasswordHandler( mysession.BaseHandler):
    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def post(self):

        sess = Session()

#       Dont think that this would actually occur
#       As change password only shows up in the captain logged in
        if(not sess.get(keyname='user') ):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<center>")
          self.Writeln("<h1>Please Login </h1>")
          self.Writeln("</center>")          
          return

        fname = sess['fname'] 
        lname = sess['lname'] 
        captain_keyname = sess['keyname'] 
        g = datastore.Captain.get_by_key_name( captain_keyname )
#       self.Writeln('password = ' + g.password)

        pw1 = self.request.get('pw1')
        pw2 = self.request.get('pw2')
        if( len(pw1) < 1 or len(pw2) < 1): 
           self.Writeln('longer password')
           return

        if( pw1 != pw2 ):
           self.Writeln('passwords don&#39;t match')
           return


        self.Writeln('Password changed')
        g.password=pw1
        db.put(g)

class UnReserveHandler(mysession.BaseHandler):
    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)


    def post(self):

# SESSION
        LoggedIn =  False

        if( self.session.get('user') ):     # (NEWSESSION)
           LoggedIn=True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 


        if(LoggedIn == False ):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<center>")
          self.Writeln("<h1>Please Login </h1>")
          self.Writeln("</center>")          
          return

#  Should only get to here is there's a session 
        fname = self.session['fname'] 
        lname = self.session['lname'] 
        captain_keyname = self.session['keyname'] 


        self.Writeln("<html>")
        try:
          keyname = self.request.get('keyname')
          if( len(keyname) == 0):
            self.Writeln("<body bgcolor=#d2d2ee>")
            self.Writeln("<center><p><br><p><br>")
            self.Writeln("<h2>Please make a selection</h2>" )
            return
        except:
          self.Writeln("<h2>Please make a selection.</h2>" )
          return


#  Get the court and set the owner to None
        e = datastore.CourtTime.get_by_key_name( keyname )

        if( type(e.owner) is types.NoneType):
            self.Writeln("<body bgcolor=#d2d2ee>")
            self.Writeln("<center>")
            self.Writeln("<h2> Can't delete reservation </h2>")
            self.Writeln("<h2> Please go back and refresh the page </h2>")
            return


        e.owner = None
        db.put( e) 

#       use to return to calender month/year
#  TODO  decide if to  implement in captain_unreserve.html page
        Month = e.date.month
        Year = e.date.year

        g = datastore.Captain.get_by_key_name( captain_keyname )
        g.count = g.count - 1
        count = g.count
        db.put( g) 

        template_values = {

#           'LoginForm' : library.LoginForm(),
            'Host'     : library.Host(),
            'Month'    : Month,
            'Year'     : Year,
            'Count'    : count,
            'Weekday'  : e.weekday,
            'Day'      : library.cday(e.start),
            'Start'    : library.ctime(e.start),
            'End'      : library.ctime(e.end),
            'Desc '    : e.desc
        }

        path = os.path.join(os.path.dirname(__file__), 'captain_unreserve.html')
        self.response.out.write(template.render(path, template_values))



class CaptainHandler( mysession.BaseHandler):


    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self ):

        capt_keyname=""


# SESSION
        LoggedIn =  False
        User = Team = ""
        path = os.environ['PATH_INFO']

        if( self.session.get('user') ):     # (NEWSESSION)
           LoggedIn=True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 

# SESSION


# Get the list of captains
        query="select __key__ from Captain order by team"
        keys =  db.GqlQuery( query)
        res = db.get(keys)
        CaptainList = []
        for r  in res:
           c = Captain()
           c.fname = r.fname
           c.lname = r.lname
           c.user =  r.user
           c.team =  r.team

           CaptainList.append( c )
# 

        CaptainReservation = Reservation()        
        user = self.session.get('user')  #Captain name (that's all we need)      
        if( user != None ):
           LoggedIn = True
           capt_keyname = self.session['keyname'] 
           CaptainReservation.fname = self.session['fname']
           CaptainReservation.lname = self.session['lname']
           CaptainReservation.team = self.session['team']
           g = datastore.Captain.get_by_key_name( capt_keyname )
           CaptainReservation.count = g.count

# TODO  more efficient db grab
           query="select __key__ from CourtTime where owner='" + capt_keyname + "'" + " order by date "
           keys =  db.GqlQuery( query)
           res = db.get(keys)
           courtlist = []
           for r  in res:
              c = Court()
              c.weekday = r.weekday
              c.date = library.cday(r.date)
              c.start = library.ctime(r.start)
              c.end = library.ctime(r.end)
              c.courts = library.listconv(r.courts)
              c.location = library.location(r.location)
              c.desc = r.desc
              c.key = r.key().name()
              courtlist.append( c)

           CaptainReservation.courts = courtlist

# ---------------------------------------------------------------------------------
        template_values = {
             'Host' : "/",

             'LoggedIn': LoggedIn,
             'User' : User,
             'Team' : Team,
             'path' : path,
          
             'CaptainList': CaptainList,
             'CaptainReservation': CaptainReservation,
             'Site'      : library.Host() + "/unreserve",
        }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'captain.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
          [  ('/captain', CaptainHandler),
             ('/unreserve', UnReserveHandler),
             ('/pwchange', PasswordHandler),
          ], debug=True , config=mysession.config)



