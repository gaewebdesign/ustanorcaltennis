import webapp2  # (NEWSESSION)
import mysession # (NEWSESSION)

import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

import urllib
import re,cgi,calendar,string,types
import datetime,time

import datastore,library

from google.appengine.api import users

weekday=["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]

# this is also in create.py (NEWSESSION)
def add_underscore( clist):
   _str = ""
   for c in clist:   
     _str = _str + "_" + c

   return _str


def monday( m,d, y):
   return datetime.date(m,d,y) - datetime.timedelta( datetime.date(m,d,y).weekday())


def court_list( clist):
   _list=[]
   for c in courtlist:   
      _list.append( c)

   return _list


class Hours(object):
  def __init__(self,hr):
     self.hr = hr
     if( hr < 12):
         self.p = str(hr) + "am"
     elif( hr == 12) :
         self.p = "12 noon"
     else:
         self.p = str(hr-12)+"pm"


class Days(object):
  def __init__(self,d):
     self.day = d
     self.selected = ""

class Months(object):
  def __init__(self,n,m):
     self.number = n
     self.month = m

class Captains:
     fname=""     
     lname=""     
     user=""     
     team=""
     password=""
     count=0
     key=""

class DeleteHandler(webapp2.RequestHandler):
    def get(self ):
        print("delete schedules")
        query="select __key__ from CourtTime "
        keys =  db.GqlQuery( query)
        for k in keys:
          p = db.get(k)
          print("delete", p.date, p.weekday)
          db.delete(k)

class OpenHandler(webapp2.RequestHandler):

    def Writeln(self,t):
        self.response.out.write(t+"\n")

    def post(self):

        _month = cgi.escape(self.request.get('open_month'))
        _hour = cgi.escape(self.request.get('open_hour'))
        _day = cgi.escape(self.request.get('open_day'))
        _year = cgi.escape(self.request.get('open_year'))

        self.Writeln('<center>')
        self.Writeln( str(_month)+'/'+str(_day) + '/'+str(_year) )

        key_id =  "key_opendate"
        g = datastore.OpenDate( key_name=key_id )
        g.openingdate= datetime.datetime(year=int(_year), month=int(_month), day=int(_day),hour=int(_hour),minute=0)
        db.put( g )

class AddCaptHandler(webapp2.RequestHandler):

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def post(self):

        fname = cgi.escape(self.request.get('fname'))    
        lname = cgi.escape(self.request.get('lname'))    
        user = cgi.escape(self.request.get('user'))    
        team = cgi.escape(self.request.get('team'))    
        password = cgi.escape(self.request.get('password'))    


        key_id =  "key_"+ fname + "_" + lname  + "_" + team
        g = datastore.Captain( key_name=key_id )
        g.count = 0
        g.fname = fname
        g.lname = lname
        g.user = user
        g.password = password
        g.team = team
        print( fname,lname,user,team,password )
#       print( g.fname,g.lname,g.user,g.team,g.password )

        db.put( g )



class EditCaptHandler(webapp2.RequestHandler):

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def post(self):
        self.Writeln("posted<br>")
        _arg = self.request.arguments() 
#       self.Writeln( str(len( _arg )) )
#       self.Writeln( str( _arg ) )

        for e in _arg:
           _rest = self.request.get_all(e)
           keyname  = _rest[0]
           password = str(_rest[1])
           count    = int(_rest[2])
           self.Writeln( str(keyname) + " " + str(password) + " " + str(count) + "<br>" )
           user = datastore.Captain.get_by_key_name( keyname )

           if( user != None):
             user.password = password
             user.count    = count
             db.put(user)
           else:
             self.Writeln( " couldnt get captain " )



# Do the entire season's schedule
class SeasonHandler(webapp2.RequestHandler):
    def Write(self,t):
     self.response.out.write(t)

    def Writeln(self,t):
     self.response.out.write(t)
     self.response.out.write("<br>")

    def get(self):
     self.Writeln("Season's Schedule")

     self.Adults( datetime.datetime( 2012, 3, 26  ) , 14 ) # year, month,day for  x weeks

    def Adults(self,start, weeks):
     pass


class ScheduleHandler(webapp2.RequestHandler):

    def Write(self,t):
     self.response.out.write(t)

    def Writeln(self,t):
     self.response.out.write(t)
     self.response.out.write("<br>")

    def get(self):

        dayofmonth = []
        for d in range(1,32):
          _d =  Days(d) 
          if( d == 9 ) : _d.selected="selected"
          dayofmonth.append( _d )

        m = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sept","Oct","Nov","Dec"]
        mon=[]
        for d in range(0,len(m)):
          mon.append( Months(d+1,m[d]) )


        hlist = []
        for d in range(8,23):
          hlist.append( Hours(d) )

        p = datastore.OpenDate.get_by_key_name( "key_opendate" )


        opendate = None
        opentime = None

        if( p ):
         opendate = p.openingdate
         opentime = library.ctime(p.openingdate)

#       Get all the Captains
        query="select __key__ from Captain order by team"

        clist=[]
        Captainkeys =  db.GqlQuery( query)
        for key in Captainkeys:
           c = Captains()
           k = db.get(key)
           c.fname = k.fname
           c.lname = k.lname
           c.user = k.user
           c.team = k.team
           c.password = k.password
           c.key = k.key().name()
           c.count = k.count
           clist.append(c)

#       g.date= datetime.datetime(year=int(_year), month=int(_month), day=int(_day),hour=20,minute=0)

        site = library.Host()
        template_values = {
             'Site': site,
             'Hours': hlist,
             'Days': dayofmonth,
             'Months': mon,
             'opendate': opendate,
             'opentime': opentime,
             'Captains' : clist

        }
        path = os.path.join(os.path.dirname(__file__), 'templates', 'administer.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

#       weekday = [ "Mon","Tues","Wed", "Thurs", "Fri", "Sat","Sun"]

        weeks = cgi.escape(self.request.get('weeks'))            #  weeks
        days4 = cgi.escape(self.request.get('days4'))            #  either 0 or 4 (Mon-Thurs)

        split = cgi.escape(self.request.get('split'))            #  blank, a or b
        if( split == "a" or split == "b"): split="_" + split

        location = cgi.escape(self.request.get("location"))      #  blank, a or b


        description = cgi.escape(self.request.get('desc'))

        start_hr = cgi.escape(self.request.get('start_hr'))
        t = start_hr.split(":")
        start_hr = int(t[0])
        start_min="0"
        if( len(t)>1): start_min = t[1]
        start_min = int(start_min)


        start_len = int(cgi.escape(self.request.get('start_len')))
        courtlist = self.request.get_all('courts')
        month =  self.request.get('m') 
        day   =  self.request.get('d') 
        year  =  self.request.get('y') 

#       courts=[]
#       court_str = ""
#
#       for c in courtlist:   
#           court_str = court_str + "_" + c
#           courts.append( c)

        court_str = add_underscore( courtlist )

# TODO  STOP IF NO COURTS SELECTED!

        try:
         start= datetime.datetime(year= int(year) , month=int(month) ,day=int(day))
        except:
         self.Writeln("EXCEPTION: date error" )
         return

#  0:Monday 1:Tues 2:Wed 3:Thurs 4:Fri 5:Sat 6:Sun
        d = start.weekday() 
        self.Writeln("start.weekday() = " + str(d) )

        if( int(days4) == 4):
         start = start - datetime.timedelta( days = d)       # Starts on Monday
         self.Writeln("should start on Monday " + start.strftime("%A") )
         print("should start on Monday " + start.strftime("%A") )


        if( int(days4) == 2):   #Starts on Saturday
         start = start - datetime.timedelta( days = d) + datetime.timedelta( days=5 )
         self.Writeln("should start on Saturday " + start.strftime("%A") )
         print("should start on Saturday " + start.strftime("%A") )


        reservelist=[]
        for w in range(0 , int(weeks)):
          self.Writeln("week  " + str(w))
          for d in range(0,int(days4)):
            reserve= start + datetime.timedelta(days = w*7 + d)
            rstart = reserve + datetime.timedelta(hours= start_hr, minutes=start_min)
            rend = reserve + datetime.timedelta(hours= start_hr + start_len,minutes=start_min)

            key_id =  "_"+ string.replace(str(rstart) ," " ,"_") + court_str + "_" + weekday[reserve.weekday()] + "_" +location+ split

            g = datastore.CourtTime( key_name=key_id )
            g.date = reserve
            g.start = rstart
            g.end = rend
#           g.courts = courts
            g.courts = courtlist
            g.location = location
            g.desc = description
            g.weekday  = weekday[ reserve.weekday() ]
            g.owner = None
            reservelist.append(g)

            self.Writeln(" append " + key_id )


        db.put( reservelist )


# ADMIN  Delete reservation
class Reservation:
        day    = ""
        date   = ""
        rstart = ""
        rend   = ""
        courts = ""
        desc   = ""

class DeleteCourtHandler(webapp2.RequestHandler):

    def get(self,url):

        query="select __key__ from CourtTime order by date"
        keys =  db.GqlQuery( query)
       
        clist=[]
        for k in keys:
          r = db.get(k)

          d =  Reservation()

          d.date   = r.date
          d.day    = weekday[r.date.weekday()]
          d.rstart = r.start
          d.rend   = r.end
          d.courts = r.courts
          d.desc   = r.desc
          clist.append(d)


        template_values = {
                'Reservation': clist

        }

        path = os.path.join(os.path.dirname(__file__), 'deletecourts.html')
        self.response.out.write(template.render(path, template_values))



app = webapp2.WSGIApplication(
                                     [('/admin', ScheduleHandler ),
                                     ('/doschedule', ScheduleHandler ),
                                     ('/season', SeasonHandler),
                                     ('/doopen', OpenHandler),
                                     ('/doeditcapt', EditCaptHandler),
                                     ('/doaddcapt', AddCaptHandler),
                                     ('/delete', DeleteHandler ),
                                     ('/(deletecourt)', DeleteCourtHandler),

                                     ],

                                     debug=True , config=mysession.config)



