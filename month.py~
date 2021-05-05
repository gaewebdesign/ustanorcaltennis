import webapp2  # (NEWSESSION)

from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types

import datastore,library

#from appengine_utilities.sessions import Session # (NEWSESSION)

# http://www.fiveriversyoga.com/a-dedicated-life-practice

import mysession # (NEWSESSION)

class Day:
    year=2012    
    month=1    
    day=1    
    classtype=""
    holiday = ""
    courts = ""

class Courts:
    time=""
    cts = ""
    owner= ""
    location = ""
    mine = False



class MonthHandler( mysession.BaseHandler):


    def Writeln(self,t):
        self.response.out.write(t+"\n")

    def Write(self,t):
        self.response.out.write(t)

# FindCourts has to be with mysession.BaseHandler for SESSION to work (to identify court owner Captain)
    def FindCourts( self, y,m,d):


        d = "DATETIME(" + str(y) + "," + str(m) + "," + str(d) + ")"
        query="select __key__ from CourtTime where date= " + d
        keys =  db.GqlQuery( query)
        r = []

        for k in keys:
           p = db.get(k)
           c = Courts()
           c.time = library.stime(p.start)  

           c.location = p.location   #RWO location updated 2/1/2019 

#          print("keyname = " + self.session['keyname'])
           if( type(p.owner) is types.NoneType): 
             c.cts  = library.listconv(p.courts)
             c.cts  = c.cts # + " " + p.location    # Add the location (Mg = Mango)
           else:
             g = datastore.Captain.get_by_key_name( p.owner )
#            print("keyname = " + g.key().name )
             c.cts = g.fname

# SESSION  Check here if the session user owns the court
             if( self.session.get('user') ):     # (NEWSESSION)
                  if( self.session['keyname'] == g.key().name() ):
                    c.mine=True

           r.append( c)

        return r


    def get(self ,month,year):

# SESSION
        LoggedIn = False
        User = Team = ""
        path = os.environ['PATH_INFO']
        for key in os.environ :
         print( key + "->" + str(os.environ[key])  )

 
# SESSION
        print( " ^ "*30 )
        print( self.session.get('user') )
        print( " v "*30 )


        if( self.session.get('user') ):     # (NEWSESSION)
           LoggedIn=True
           User = self.session['fname'] + " " + self.session['lname'] 
           Team = " (" + self.session['team'] + ")" 

        m = ["Jan","January","February","March","April","May","June","July","August","September","October","November","December"]

        month=int(month)
        year=int(year)

# Figure next month/year    
        next_month = month + 1
        next_year = year 
        if( next_month > 12):
               next_month = 1
               next_year = year + 1

# Figure previous month/year    
        prev_month = month - 1
        prev_year  = year 
        if( prev_month < 1):
               prev_month = 12
               prev_year = year - 1

#Properly initialize calenddar to start on SUNDAY
        calendar.setfirstweekday( calendar.SUNDAY)
        cal = calendar.Calendar(calendar.SUNDAY)

# Calculate the few days before/after this month
        offdays=[]
        for d in cal.itermonthdates(year , month ):
            if( not re.search(str(year)+"-[0]*"+str(month) ,str(d) ) ):
                   offdays.append( d)   # list of datetime objects

# -----------------------------------------------------------------------
        thismonth = calendar.monthcalendar(year, month ) 
        nweeks = len(thismonth) 

        index=0
        Reservations=[]                 # Array of weeks
        for w in range(0,nweeks):       # 0,1,2,3,4
            week = thismonth[w]             # list of days of each week (0,0,0,0,1,2,3), (4,5,6,7,8,9,10)
            wk = []
            for x in week:   # either 0 (days before) or current day (1..31)
                 d  = Day()
                 d.day = x

                 d.classtype = "weekday"
                 if( x==0 ): 
                    d.classtype = "previous"
                    t = offdays[index]
                    d.day= t.day
                    d.month = t.month
                    d.year  =  t.year
                    index   = index + 1
                 else:
                    _d = calendar.weekday(year,month,x)
                    if( _d == 5 or _d == 6):  d.classtype = 'weekend' 
                    d.day = x
                    d.month = month
                    d.year = year


                 d.holiday = library.Holiday(d.year,d.month,d.day)
                 d.courts = self.FindCourts(d.year , d.month , d.day)
                 wk.append(d)

            Reservations.append(wk)           
            StartDate = StartTime = None;
            Start =  library.GetReservationStart ( )
            if(Start != None):
               StartDate = Start[0]
               StartTime = Start[1]

        template_values = {
               'monthname'     : m[month],
               'month'     : month,
               'year'      : year,

               'LoggedIn'  : LoggedIn,
               'User' : User,
               'Team' : Team,
               'path'      : path,

               'StartDate' : StartDate,
               'StartTime' : StartTime,

               'Next_month'     : next_month,
               'Next_year'      : next_year,
               'Prev_month'     : prev_month,
               'Prev_year'      : prev_year,
               'Month'            : Reservations,

        }

        path = os.path.join(os.path.dirname(__file__), 'templates','month.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
          [  ('/month/([\d]*)/([\d]*)', MonthHandler)
          ], debug=True , config=mysession.config)

