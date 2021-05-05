import webapp2 #(NEWSESSION)

#from google.appengine.ext import webapp


from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types

import datastore,library

#from appengine_utilities.sessions import Session
import mysession #(NEWSESSION)

class Reservation:
   fname=""              # Captain name
   lname=""              # Captain name
   team=""               # team
   courts=[]             # court list 


class Court:
   weekday=""            # day of week
   date=""               # date of reservation

   courts=""             # courts (string)
   start=""              # start time   (converted to am/pm)
   end=""                # end time     (converted to am/pm)
   desc=""               # description  

   captain=""            # 
   team=""               # 


class ByDateHandler(webapp2.RequestHandler):


    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self ):

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

        template_values = {
            'Courts': courtlist
        }

        path = os.path.join(os.path.dirname(__file__), 'bydate.html')
        self.response.out.write(template.render(path, template_values))

class ByCaptainHandler(webapp2.RequestHandler):


    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self ):

        Others=[]   # Others is an array captains
        OtherTeams=[]   # Others is an array of Reservation()
        query="select __key__ from Captain order by lname"
        keys =  db.GqlQuery( query)
        captains = db.get(keys)
        for e in captains:

            keyname =  e.key().name() 
#           Skip if its the logged in captain 
            if( keyname == capt_keyname ): continue

            Others.append( e )
            query="select __key__ from CourtTime where owner= '" + keyname  + "'"      
            keys =  db.GqlQuery( query)
            res = db.get(keys)
#           Get the courts
            courtlist=[]
            for  r in res:
              c = Court()
              c.weekday = r.weekday
              c.date = library.cday(r.date)
              c.start = library.ctime(r.start)
              c.end = library.ctime(r.end)
              c.courts = library.listconv(r.courts)
              courtlist.append( c)

            teamreserve= Reservation()           # make an instance
            teamreserve.fname = e.fname          # Captan's name
            teamreserve.lname = e.lname          
            teamreserve.team = e.team            # Captain's team
            teamreserve.courts= courtlist        # list of reserved courts

            OtherTeams.append( teamreserve )


class InstructionHandler( mysession.BaseHandler ):


    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self ):

        capt_keyname=""
        LoggedIn =  False
        User = Team = ""
        path = os.environ['PATH_INFO']

        CaptainReservation = Reservation()        

        if(self.session.get('user') ):     # (NEWSESSION)

           LoggedIn = True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 


           capt_keyname = self.session['keyname'] 
           CaptainReservation.fname = self.session['fname']
           CaptainReservation.lname = self.session['lname']
           CaptainReservation.team  = self.session['team']

# TODO  more efficient db grab
           query="select __key__ from CourtTime where owner='" + capt_keyname + "'"
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
              courtlist.append( c)

           CaptainReservation.courts = courtlist

# ---------------------------------------------------------------------------------
        query="select __key__ from CourtTime order by date"
        keys =  db.GqlQuery( query)
        bydate=[]
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

                bydate.append( c)


# ---------------------------------------------------------------------------------
        template_values = {
             'LoggedIn': LoggedIn,
             'User' : User,
             'Team' : Team,
             'path' : path,


             'CaptainReservation': CaptainReservation,
             'ByDate': bydate,
#            'OtherTeams': OtherTeams
        }

        path = os.path.join(os.path.dirname(__file__),'templates', 'instructions.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
          [  ('/instructions', InstructionHandler)
          ], debug=True , config=mysession.config)

