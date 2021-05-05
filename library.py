# from appengine_utilities.sessions import Session (OLDSESSION)

import urllib,sys,re,string,datetime,os
import datastore

import logging  #(NEWSESSION)

months= ("January", "January", "February", "March", "April", "May", "June", "July","August", "September","October", "November", "December")

def getDate( d ):
   year= str(d.year)
   month=months[(d.month)]
   day=str(d.day)

   return  month + " " + day + ", " + year


# Convert from military to standard time
def stime( d ):
 hour = d.hour
 minute = d.minute

 z =""
 if( minute<10): z="0"
 if( hour > 12):    hour = hour - 12
 r = str(hour) + ":" + z + str(minute)
 return r


def ctime( d ):
 hour = d.hour
 minute = d.minute

 z =""
 if( minute<10): z="0"

 pm = " am"
 if( hour == 12):
       pm = " pm"
 elif( hour > 12):
       pm= " pm"
       hour = hour - 12

 r = str(hour) + ":" + z + str(minute) + str(pm)
 return r



def cday( d ):
   year= str(d.year)
   month=str(d.month)
   day=str(d.day)

   return  month + "-" + day + "-" + year


def Host():
# HTTP_HOST also works
#        url = os.environ["SERVER_NAME"]
#        for e in os.environ:
#           self.Writeln(e + " " + os.environ[e] + "<br>")

    url = "http://"+os.environ["SERVER_NAME"]
    if (re.search("localhost",url )): url = "http://localhost:8080"

    return url


def LoginForm(  ):

    sess = Session()
    if( sess.get(keyname='user') ):
        site = Host() + "/logout"
        form = '<form name="logout" action="'+site +'" method="POST">'

        form = form + '<input type="hidden" name="path" value ="'+ os.environ["PATH_INFO"] +'">'
        form = form + '<input type="submit" value="Logout">'
        form = form + '&nbsp;'
        form = form + sess['fname'] + " " +  sess['lname']  + " logged in"
        form = form + " for " +  sess['team']
        form = form + '</form>'
        return form

    site = Host() + "/login"
    form = '<form name="login" action="'+site +'" method="POST">'
    form = form +'&nbsp;'
    form = form + '<input type="hidden" name="path" value ="'+ os.environ["PATH_INFO"] +'">'
    form = form +'<input type="submit" value="Login">'
    form = form +'<input type="text" id="e50"  size="7" name="username">' 
    form = form +'&nbsp;'
    form = form +'<input type="password" id="e50" size="7" name="password">'
    form = form +'&nbsp;'
    form = form +'</form>'
#   form = form +'</div>'

    return form


def listconv( alist ):
   r=""
   for a in alist: r = r + a + ","

   if( r != ""): r = r.rstrip(",")

   return r


def GetReservationStart ( ):

        g = datastore.OpenDate.get_by_key_name(  "key_opendate" )
        if( g == None):
          return None

        start = g.openingdate

        StartDate    = getDate(g.openingdate)
        StartTime    = ctime(g.openingdate)

        return [ StartDate, StartTime ]


def location( where):
       loc="LP"
       if( re.search("Wash",where,re.IGNORECASE)): loc="WASH"
       if( re.search("Lowell",where,re.IGNORECASE)): loc="Lowell"
       if( re.search("Mg",where,re.IGNORECASE)): loc="Mango"
       if( re.search("Cu",where,re.IGNORECASE)): loc="Cuesta"
       return loc


def Holiday( y,m,d):

#  if(y==2015 and m==12 and d==25): return os.environ['HOMECOURTS']

  dates = [


          ([2015,12,25],"Christmas"),
          ([2016,5,8],"Mothers Day"),
          ([2016,6,4],"4th July"),

          ([2016,1,4],"Week 1"),

          ([2016,4,8],"40Mx"),
          ([2016,4,9],"1st Round"),
          ([2016,4,10],"Playoffs"),

          ([2016,4,22],"40Mx"),
          ([2016,4,23],"2nd Round"),
          ([2016,4,24],"Playoffs"),

          ([2016,4,22],"40Mx"),
          ([2016,4,23],"Sectionals"),
          ([2016,4,24],"Weekend"),

          ([2016,6,24],"Adults"),
          ([2016,6,25],"1st Round"),
          ([2016,6,26],"Playoffs"),

          ([2016,7,8],"Adults"),
          ([2016,7,9],"2nd Round"),
          ([2016,7,10],"Playoffs"),

          ([2016,8,5],"Adults"),
          ([2016,8,6],"Districts"),
          ([2016,8,7],"Weekend"),

          ([2016,8,26],"Adult Sectionals"),
          ([2016,8,27],"SouthBay"),
          ([2016,8,28],"NTRP"),

  ]




  for k in dates :
     if( k[0] == [y,m,d]):
           return k[1]

# IF nothing happpening today, return "Today"
  today = datetime.datetime.now() - datetime.timedelta( hours = 8)
  if( [today.year,today.month,today.day] == [y,m,d] ):
           return "Today"

  return ''


