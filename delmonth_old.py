import webapp2  # (NEWSESSION)

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types

import datastore,library
#from appengine_utilities.sessions import Session
import mysession # (NEWSESSION)


# http://www.fiveriversyoga.com/a-dedicated-life-practice


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
    key= ""
    mine = False

# ---------------
#   day = ""
    start = ""
    end = ""
    location = ""
    courts = ""
    desc = ""
    open = True



# Search for courts for  y/m/d 
def FindCourts (y , m , d):
        d = "DATETIME(" + str(y) + "," + str(m) + "," + str(d) + ")"
        query="select __key__ from CourtTime where date= " + d
        keys =  db.GqlQuery( query)

        r = []
        for k in keys:
           p = db.get(k)
           c = Courts()
           c.time = library.stime(p.start)  
           c.key = k

           if( type(p.owner) is types.NoneType): 
             c.cts  = library.listconv(p.courts)
             c.cts  = c.cts # + " " + p.location    # Add the location (Mg = Mango)
           else:
             g = datastore.Captain.get_by_key_name( p.owner )
             c.cts = g.fname
             sess = Session()
             if( sess.get(keyname='user') ):
                  if(sess['keyname'] == g.key().name()):
                         c.mine = True             # To put in boldface (in html)
#                        sess.delete()
# TODO  Keep track of this session  - does it affect Login?                

           r.append( c)

        return r


# Put any holidays or other special dates in here
def Holiday( y,m,d):
  
  if(y==2012 and m==1 and d==2): return "Start"   
  if(y==2012 and m==2 and d==14): return 'Valentines Day'   
  if(y==2012 and m==5 and d==13): return "Mother's Day"   

  if(y==2012 and m==3 and d==26): return 'Week 1'   
  if(y==2012 and m==6 and d==25): return 'Week 14'   

#  if(y==2012 and m==4 and d==2):  return 'Week 2'   
#  if(y==2012 and m==4 and d==9):  return 'Week 3'   
#  if(y==2012 and m==4 and d==16):  return 'Week 4'   
#  if(y==2012 and m==4 and d==23):  return 'Week 5'   

  return ''


class DisplayCourtHandler( mysession.BaseHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self,month,day, year):
        pass

        d = "DATETIME(" + year + "," + month + "," + day + ")"
        query="select __key__ from CourtTime where date= " + d
        keys =  db.GqlQuery( query)
        courtlist=[]
        for k in keys:
          p = db.get(k)
          c = Courts()
          c.day = library.cday(p.start)                   
          c.start = library.ctime(p.start)                   
          c.end = library.ctime(p.end)                   
          c.desc = p.desc
          c.key = k
          c.courts = library.listconv( p.courts) 
          c.location = library.location(p.location)
          c.open = True
          if( type(p.owner) is not  types.NoneType):
             g = datastore.Captain.get_by_key_name( p.owner )
             c.owner = g.fname
             c.open = False

          courtlist.append( c )

        template_values = {
            'month'   : month,
            'day'     : day,
            'year'    : year,
            'Courtlist' : courtlist,
            'LoginForm' : library.LoginForm(),
#           'Site'      : library.Host() + "/reserve",
#           'Key'       :  k
        }

        path = os.path.join(os.path.dirname(__file__), 'delcourts.html')
        self.response.out.write(template.render(path, template_values))


class DelMonthHandler( mysession.BaseHandler ):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def post(self ):

        sess = Session()
        if(not sess.get(keyname='user') ):
          self.Writeln("<p><br><p><br>")
          self.Writeln("<center>")
          self.Writeln("<h1>Please Login </h1>")
          self.Writeln("</center>")          
          return

        fname = sess['fname'] 
        lname = sess['lname'] 

        if( not( fname =='Roger') ):
           self.Writeln("<h1>Cant Delete Court Reservations </h1>")
           return


        reservation = self.request.get_all('reservation')

        for r in reservation:
           p = db.get(r)
           self.Writeln(p.weekday + " " + str(p.date) + " " + str(p.start) + " " + str(p.courts) +  "  " + str(p.desc)  )
           self.Writeln("<br>")
           db.delete(r)


    def get(self ,month,year):
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

# Calculate the few days before/after this month
        offdays=[]
        cal = calendar.Calendar()
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
                 d.courts = FindCourts(d.year , d.month , d.day)
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
               'LoginForm' : library.LoginForm(),
               'Host'      : library.Host(),

               'StartDate' : StartDate,
               'StartTime' : StartTime,

               'Next_month'     : next_month,
               'Next_year'      : next_year,
               'Prev_month'     : prev_month,
               'Prev_year'      : prev_year,
               'Month'            : Reservations,

        }

        path = os.path.join(os.path.dirname(__file__), 'delmonth.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication(
             [ 

               ('/delmonth/([\d]*)/([\d]*)', DelMonthHandler),
               ('/dodelmonth', DelMonthHandler),
               ('/_courts/([\d]*)/([\d]*)/([\d]*)', DisplayCourtHandler)

          ], debug=True , config=mysession.config)




