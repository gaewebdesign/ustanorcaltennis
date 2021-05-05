
import webapp2  # (NEWSESSION)

from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types,time

import datastore
import library

#from appengine_utilities.sessions import Session

import mysession # (NEWSESSION)

class Court:
    day = ""
    start = ""
    end = ""
    courts = ""
    location = ""
    desc = ""
    key = ""
    open = True


class Court_old:

 def __init__(self,day,courts,start,end,desc,key):
  self.day   = library.cday(start)
  self.start = library.ctime(start)
  self.end   = library.ctime(end)

  self.courts  = ""
  for e in courts:
   self.courts  = self.courts + e + ","
  
# TODO - more efficient way to rid of last (,) comma
  if( self.courts != ""):
     self.courts = self.courts.rstrip(",")

  self.desc  = desc
  self.key   = key




class CourtHandler( mysession.BaseHandler):

    def Writeln(self,t):
        self.response.out.write(t+"\n")

    def get(self, month,day,year):

        LoggedIn = False
        User = Team = ""
        path = os.environ['PATH_INFO']

        if( self.session.get('user') ):     # (NEWSESSION)
           LoggedIn=True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 


        d = "DATETIME(" + year + "," + month + "," + day + ")"
        query="select __key__ from CourtTime where date= " + d
        keys =  db.GqlQuery( query)

        available=False
        courtlist=[]
        for k in keys:
          p = db.get(k)
#         c = Court_old( p.weekday,p.courts, p.start, p.end, p.desc , k )          

# DONE REFACTORed to Court
          c = Court()
          c.day = library.cday(p.start)                   
          c.start = library.ctime(p.start)                   
          c.end = library.ctime(p.end)                   
          c.desc = p.desc
          c.key = k
          c.courts   = library.listconv( p.courts) 
          c.location = library.location(p.location)
          c.open = True
          if( type(p.owner) is not  types.NoneType):
             g = datastore.Captain.get_by_key_name( p.owner )
             c.owner = g.fname
             c.open = False

          courtlist.append( c )
          if( c.open == True): available = True

        template_values = {
            'month'   : month,
            'day'     : day,
            'year'    : year,

            'LoggedIn'  : LoggedIn,
            'User' : User,
            'Team' : Team,
            'path'      : path,

            'Courtlist' : courtlist,
            'Available'      : available


        }

        path = os.path.join(os.path.dirname(__file__),'templates', 'courts.html')
        self.response.out.write(template.render(path, template_values))



class ReserveHandler( mysession.BaseHandler):

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def post(self):

        LoggedIn = False
        User = Team = ""
        path = os.environ['PATH_INFO']

        if( self.session.get('user') ):     # (NEWSESSION)
           LoggedIn=True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 


        if(LoggedIn == False ):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<body bgcolor=d2d2ff>")
          self.Writeln("<center>")
          self.Writeln("<h1>Please Login </h1>")
          self.Writeln("</center>")          
          return

        courts = self.request.get('courts')
        if( courts == ""):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<body bgcolor=d2d2ff>")
          self.Writeln("<center>")
          self.Writeln("<h1>Please Select Courts </h1>")
          self.Writeln("</center>")          
          return

        e = db.get( courts)
#       This shouldn't ever happen since reserved court can't be selected
        if( type(e.owner) is not types.NoneType):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<body bgcolor=d2d2ff>")
          self.Writeln("<center>")
          self.Writeln("<h1>Courts already Selected </h1>")
          self.Writeln("</center>")          
          return

# -------------------------------------------------------------------
#       By now, use has logged in and selected courts

# (NEWSESSION)
        captain_keyname = self.session['keyname']
        Captain = datastore.Captain.get_by_key_name( captain_keyname )
        CourtTime = ""

        g = datastore.OpenDate.get_by_key_name(  "key_opendate" )
        if( g == None):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<center>")
          self.Writeln("<body bgcolor=d2d2ff>")
          self.Writeln("WARNING! Set Opening Date For Reservations")
          return

        start = g.openingdate

        StartDate    = library.getDate(g.openingdate)
        StartTime    = library.ctime(g.openingdate)
        Today   = library.getDate(datetime.datetime.utcnow() - datetime.timedelta(hours=8))
        Today   =  Today + " @" + library.ctime(datetime.datetime.utcnow() - datetime.timedelta(hours=7))

        delta   = datetime.datetime.utcnow() - datetime.timedelta(hours=8) - start

        if( datetime.datetime.utcnow() - datetime.timedelta(hours=8) < start  ):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<center>")
          self.Writeln("<body bgcolor=d2d2ff>")
          self.Writeln("<h1>Can't Reserve yet </h1>")
          self.Writeln("<h1>Today is " + Today + "</h1>")
          self.Writeln("<h1>Reservations start  " + StartDate + "@" +StartTime +"</h1>")
          self.Writeln("</center>")          
          return


        Allowed = 2 + 2* delta.days  

        sofar   = Captain.count

        if( sofar >= Allowed ):
           Exceeded = True
           template_values = {
            'Host'     : library.Host(),

            'StartDate': StartDate,
            'StartTime': StartTime,
            'Today'    : Today,
            'Allowed'  : Allowed,

            'Captain'  : Captain,
            'Exceeded'   : True
           }

           path = os.path.join(os.path.dirname(__file__), 'display_request.html')
           self.response.out.write(template.render(path, template_values))
           return

# ----------------------------------------------------------------------------------
#       Reserve the courts

#       courts is the Key to the court selected
        courts = cgi.escape(self.request.get('courts'))
        e = db.get( courts)

        CourtDate = library.getDate(e.date )
        CourtDay = e.weekday 
        CourtStart = library.ctime(e.start)
        CourtEnd   = library.ctime(e.end) 
        Courts =  library.listconv(e.courts )
        CourtDesc =  e.desc 

        Month = e.date.month
        Year = e.date.year

        e.owner=captain_keyname   # either use session value or from Captain db
        db.put(e)

        Captain.count = Captain.count+1
        db.put( Captain )


        template_values = {
            'Host'     : library.Host(),
            'Month'     : Month,
            'Year'     : Year,


            'StartDate': StartDate,
            'StartTime': StartTime,
            'Today'    : Today,
            'Allowed'  : Allowed,

            'Captain'  : Captain,
            'CourtDate'  : CourtDate,
            'CourtDay'  : CourtDay,
            'CourtStart'  : CourtStart,
            'CourtEnd'  : CourtEnd,

            'Courts'  : Courts,
#           'CourtDesc'  : CourtEnd,
            'Exceeded'   : False

        }

        path = os.path.join(os.path.dirname(__file__), 'templates','reserve.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
          [  ('/courts/([\d]*)/([\d]*)/([\d]*)', CourtHandler),
             ('/reserve', ReserveHandler),

          ], debug=True , config=mysession.config)




