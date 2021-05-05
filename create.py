from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,cgi,re,datetime,sys, calendar,string,types

import datastore,library
from appengine_utilities.sessions import Session

weekday=["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]

def add_underscore( clist):
   _str = ""
   for c in clist:   
     _str = _str + "_" + c

   return _str

def skip( day):

#  South Bay  NTRP
      if( day == datetime.datetime( 2012, 8, 24 )):  return True
      if( day == datetime.datetime( 2012, 8, 25 )):  return True
      if( day == datetime.datetime( 2012, 8, 26 )):  return True

      return False



#   All the parameters for a court reservation
def MakeCourtTime( date,rstart , rend, courts , desc , location, split):

    court_str = add_underscore( courts )
    key_id =  "_"+ string.replace(str(rstart) ," " ,"_") + court_str + "_" + weekday[rstart.weekday()] + "_" +location+ split

    g = datastore.CourtTime( key_name=key_id )
    g.date = date               # date of reservation, used to search for courts
    g.start = rstart
    g.end = rend
    g.courts = courts
    g.location = location
    g.desc = desc
    g.weekday  = weekday[ rstart.weekday() ]
    g.owner = None

    return g;
    return key_id;




def SessionCheck():

    return True

    sess = Session()
    if(not sess.get(keyname='user') ):
       return False

    fname = sess['fname'] 
    lname = sess['lname'] 

    if( not( fname =='Roger') ):
       return False

    return True

class DisplayHandler(webapp.RequestHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def get(self ):

        template_values = {
               'Host'      : library.Host(),
               'LoginForm' :  library.LoginForm()

        }

        path = os.path.join(os.path.dirname(__file__), 'create.html')

        self.response.out.write(template.render(path, template_values))

class DeleteHandler(webapp.RequestHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def deletecourts(self):
        query="select __key__ from CourtTime "
        keys =  db.GqlQuery( query)
        for k in keys:
          p = db.get(k)
          self.Writeln("delete " +  p.weekday + " " + str(p.date)  + " <br>")
          db.delete(p)


    def clearcourts(self):
        query="select __key__ from CourtTime "
        keys =  db.GqlQuery( query)
        for k in keys:
          p = db.get(k)
          if( type(p.owner) is not types.NoneType):
           self.Writeln("set " +  p.weekday + " " + str(p.date)  + " to None <br>")
           p.owner=None
           db.put(p)


    def clearcaptains(self):
        query="select __key__ from Captain"
        keys =  db.GqlQuery( query)
        for k in keys:
          p = db.get(k)
          p.count=0
          self.Writeln("Set " +  p.fname + " " +  p.lname + " to " + str(p.count) + "<br>")
          db.put(p)


    def deletecaptains(self):
        query="select __key__ from Captain"
        keys =  db.GqlQuery( query)
        for k in keys:
          p = db.get(k)
          p.count=0
          self.Writeln("Set " +  p.fname + " " +  p.lname + " to " + str(p.count) + "<br>")
          db.delete(p)


    def post(self ):

        if( SessionCheck() == False):  
           self.Writeln("not authorized ")
           return

        self.Write("post")
        delete = self.request.get_all('delete')

        for r in delete:
          if( r == 'clrcourts'):
            self.Write("Clear Courts <br>")
            self.clearcourts()

          if( r == 'delcourts'):
            self.Write("Delete Courts <br>")
            self.deletecourts()

# --------------------------------------------------------------------
          if( r == 'clearcaptains'):
            self.Write("Clear Captain <br>")
            self.clearcaptains() 
            self.clearcourts()


          if( r == 'delcaptains'):
            self.Write("Delete Captain <br>")
            self.deletecaptains() 
            self.clearcourts()

class CreateCaptainHandler(webapp.RequestHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")

    def Write(self,t):
        self.response.out.write(t)

    def post(self):

        if( SessionCheck() == False):  
           self.Writeln("not authorized ")
           return

        if( self.request.get('ccapt') != 'ccapt'): 
           self.Writeln("nothing selected ")
           return

        captains = []

# Cuesta Captains
        captains.append( ("Julie", "Satake Ryu" ,"julie", "julie","Mx7.0A" ) )
        captains.append( ("Vijay", "Peddada" ,"vijay7", "vijay","Mx7.0B" ) )
        captains.append( ("Kevin", "Ong" ,"kevin7", "kevin","Mx7.0C" ) )
        captains.append( ("Ken", "Fukui" ,"ken", "ken","Mx8.0A" ) )
        captains.append( ("Vijay", "Peddada" ,"vijay8", "vijay","Mx8.0B" ) )
        captains.append( ("Kevin", "Ong" ,"kevin8", "kevin","Mx8.0C" ) )
        captains.append( ("Roger", "Okamoto" ,"roger", "roger","Mx8.0D" ) )
        captains.append( ("Fulin", "Thiessen","fulin", "fulin","Mx9.0A" ) )
        captains.append( ("Howard", "Giles","howard", "howard","Mx9.0B" ) )
        captains.append( ("John", "Togasaki","john", "john","Mx10.0A" ) )
        captains.append( ("Nick", "Fustar","nick", "nick","Mx10.0B" ) )
        captains.append( ("Wesley", "Chun","wes", "wes","Mx6.0A" ) )
        captains.append( ("Melissa", "Lee","melissa", "melissa","Mx7.0D" ) )

#
        captainlist = []
        for e in captains:
          fname = e[0]
          lname = e[1]
          user = e[2]
          password = e[3]  
          team= e[4]

# replace spaces in name with _ i.e. Satake Rye
          key_fname = fname.replace(" ", "_")
          key_lname = lname.replace(" ", "_")

          key_id =  "key_"+ key_fname + "_" + key_lname  + "_" + team
          g = datastore.Captain( key_name=key_id )
          g.count = 0
          g.fname = fname
          g.lname = lname
          g.user = user
          g.password = password
          g.team = team
          captainlist.append(g)
          print( e )

        db.put(captainlist)
 
class CreateCourtsHandler(webapp.RequestHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)
        self.response.out.write("\n")
        self.response.out.write("<br>")

    def Write(self,t):
        self.response.out.write(t)

    def Adults(self, start, weeks):
#

     reservelist=[]
     for w in range( 0 , weeks):
#      self.Writeln( 'Week ' + str(w) )
       current = start + datetime.timedelta( days = 7*w)
#      self.Writeln( str(current) + " "  + dayofweek[current.weekday()] )

#      Monday-Thursday
       for d in range(0,4):
          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 18)
          rend   = day + datetime.timedelta( hours = 21)

          courts = ["1","2","3"]
          desc     = "3/2 split"
          location = "" 
          split    = "" #"a"
       
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

#---------------------------------------------------------------------------
          rstart = day + datetime.timedelta( hours = 18)
          rend   = day + datetime.timedelta( hours = 21)
          courts = ["3","4","5"]
          desc     = "2/3 split"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

#---------------------------------------------------------------------------
          rstart = day + datetime.timedelta( hours = 18)
          rend   = day + datetime.timedelta( hours = 21)
          courts = ["6","11","13"]
          desc     = "3/2 split"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )
          courts = ["13","14","15"]
          desc     = "2/3 split"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

#         self.Writeln( g ) 

       
#      Saturday,Sunday    
       for d in range(5,7):
          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 12)
          rend   = day + datetime.timedelta( hours = 14)
          courts = ["1","2","3","4","5"]
          desc     = "5 courts"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )



     db.put(reservelist)
     week = datetime.date(start.year, start.month, start.day)
     w=1
     for r in reservelist:
          
          if( datetime.date(r.start.year,r.start.month,r.start.day)  ==  week ):
             self.Writeln("Week " + str(w) )
             w = w + 1
             week = week + datetime.timedelta(days = 7 )
          self.Writeln( weekday[r.start.weekday()] + " " +str(r.start) + " " + str(r.end)  + " " + str(r.courts) + " " + r.location + " " + r.desc ) 

    def Mixed(self, start, weeks):

     reservelist=[]
     for w in range( 0 , weeks):
#      self.Writeln( 'Week ' + str(w) )
       current = start + datetime.timedelta( days = 7*w)
#      self.Writeln( str(current) + " "  + dayofweek[current.weekday()] )

#      Monday-Thursday
       for d in range(0,5):
          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 19, minutes=0)
          rend   = day + datetime.timedelta( hours = 21, minutes=0)

#         Skip this day due to other events
          if(skip( day )):   continue
          if( day==1):       continue   # Skip Tuesday

          courts = ["8","9","10"]
          desc     = "Weeknight"
          location = "Cuesta" 
          split    = "" #"a"
       
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )


#      Saturday
       for d in range(5,6):
          day = current + datetime.timedelta( days = d)

#         Skip this day due to other events
          if(skip( day )):   continue

          rstart = day + datetime.timedelta( hours = 9)
          rend   = day + datetime.timedelta( hours = 11)
          courts = ["8","9","10"]
          desc     = " 9 am"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 11)
          rend   = day + datetime.timedelta( hours = 13)
          courts = ["8","9","10"]
          desc     = "11 am"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 15 , minutes=30)
          rend   = day + datetime.timedelta( hours = 17 , minutes=30)
          courts = ["8","9","10"]
          desc     = "3 pm"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 15 , minutes=30)
          rend   = day + datetime.timedelta( hours = 17 , minutes=30)
          courts = ["8","9","10"]
          desc     = "5:30 pm"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

#      Sunday
       for d in range(6,7):
          day = current + datetime.timedelta( days = d)

#         Skip this day due to other events
          if(skip( day )):   continue

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 11)
          rend   = day + datetime.timedelta( hours = 13)
          courts = ["8","9","10"]
          desc     = "11 am"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 13)
          rend   = day + datetime.timedelta( hours = 15)
          courts = ["8","9","10"]
          desc     = "1 pm"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 15)
          rend   = day + datetime.timedelta( hours = 17)
          courts = ["8","9","10"]
          desc     = "3 pm"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )

          day = current + datetime.timedelta( days = d)
          rstart = day + datetime.timedelta( hours = 17)
          rend   = day + datetime.timedelta( hours = 19)
          courts = ["8","9","10"]
          desc     = "5 pm"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )







          rstart = day + datetime.timedelta( hours = 9)
          rend   = day + datetime.timedelta( hours = 11)
          courts = ["8","9","10"]
          desc     = " 9 am"
          g = MakeCourtTime(day, rstart , rend , courts , desc , location, split)
          reservelist.append( g )




     db.put(reservelist)
     week = datetime.date(start.year, start.month, start.day)
     w=1
     for r in reservelist:
          
          if( datetime.date(r.start.year,r.start.month,r.start.day)  ==  week ):
             self.Writeln("Week " + str(w) )
             w = w + 1
             week = week + datetime.timedelta(days = 7 )
          self.Writeln( weekday[r.start.weekday()] + " " +str(r.start) + " " + str(r.end)  + " " + str(r.courts) + " " + r.location + " " + r.desc ) 


    def post(self):

        if( SessionCheck() == False):  
           self.Writeln("not authorized ")
           return

        sel =  self.request.get('ccourt') 

        if( sel == 'Adults'): 
           self.Writeln("2012 Adults")
           self.Adults( datetime.datetime( 2012, 3, 26  ) , 14 ) # year, month,day for  x weeks
        elif( sel == 'Mixed'): 
           self.Writeln('2012 Mixed ')
           self.Mixed( datetime.datetime( 2012, 7, 2  ) , 12 ) # year, month,day for  x weeks
        elif( sel == 'Combo'): 
           self.Writeln('Combo')

        else:
           self.Writeln('Nothing selected')



def main():
    application = webapp.WSGIApplication(
          [  
               ('/create', DisplayHandler),
               ('/dodelete', DeleteHandler),
               ('/doccapt', CreateCaptainHandler),
               ('/doccourts', CreateCourtsHandler),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
  main()



#        captains.append( ("Kiran", "Kolpe" ,"kiran", "kiran","M3.0A" ) )
#        captains.append( ("Karl", "Mosgofian" ,"karl", "karl","M3.0B" ) )

#        captains.append( ("Bharat", "Krishna" ,"bahrat", "bahrat","M3.5A" ) )
#        captains.append( ("Vijay", "Peddada" ,"vijay35", "vijay35","M3.5B" ) )
#        captains.append( ("Bob", "Block" ,"bob", "bob","M3.5C" ) )

#        captains.append( ("James", "Pierce" ,"james", "james","M3.5D" ) )
#        captains.append( ("Javier", "Lavagnino" ,"javier", "javier","M4.0A" ) )
#        captains.append( ("Ken", "Fukui" ,"ken", "ken" ,"M4.0B") )
#        captains.append( ("Hong", "Wang" ,"hong", "hong" ,"M4.0E") )
#        captains.append( ("Norman", "Chow" ,"norman4", "norman4" ,"M4.0F") )
#        captains.append( ("Larry", "Lisser" ,"larry", "larry" ,"M4.0G") )
#        captains.append( ("Dana", "Anderson" ,"dana", "dana" ,"M4.0I") )
#        captains.append( ("Robert", "Brunkhorst" ,"robert", "robert" ,"M4.0C") )
#        captains.append( ("Vijay", "Peddada" ,"vijay4", "vijay4" ,"M4.0D") )
#        captains.append( ("Pak Hang", "Ho" ,"pak", "pak" ,"M4.0H") )

#        captains.append( ("Rob", "Rinsky" ,"rob", "rob" ,"M4.5A") )
#        captains.append( ("Kazu", "Kishino" ,"kazu", "kazu" ,"M4.5B") )
#        captains.append( ("Norman", "Chow" ,"norman45", "norman45" ,"M4.0F") )

#        captains.append( ("Reid", "Myers" ,"reid", "reid" ,"W3.0B") )
#        captains.append( ("Thu", "Stankunas" ,"thu3", "thu3" ,"W3.0A") )

#        captains.append( ("Rocelle", "Maliksi" ,"rocelle", "rocelle" ,"W3.5A") )
#        captains.append( ("Thu", "Stankunas" ,"th35", "thu35" ,"W3.5A") )

#        captains.append( ("Fe", "Jangraw" ,"fe4", "fe4" ,"W4.0E") )
#        captains.append( ("Maria", "Scheper" ,"maria", "maria" ,"W4.0A") )
#        captains.append( ("Alison", "Tong" ,"alison", "alison" ,"W4.0B") )
#        captains.append( ("Nancy", "Li" ,"nancy", "nancy" ,"W4.0C") )
#        captains.append( ("May", "Mu" ,"may", "may" ,"W4.0D") )
#        captains.append( ("Maria", "Ipsaro" ,"ipsaro", "ipsaro" ,"W4.0F") )

#        captains.append( ("Carrie", "Bell" ,"carrie", "carrie" ,"W4.0N") )

#        captains.append( ("Analiza", "Dolor" ,"analiza", "analiza" ,"W4.5A") )
#        captains.append( ("Lorraine", "Randall" ,"lorraine", "lorraine" ,"W4.5B") )
#        captains.append( ("Fe", "Jangraw" ,"fe45", "fe45" ,"W4.5C") )

#        captains.append( ("Roger", "Okamoto" ,"roger", "net" ,"M4.0") )
#        captains.append( ("Gary", "Caabay" ,"gary", "gary" ,"M5.0") )
#        captains.append( ("Maricar", "Caabay" ,"cai", "cai" ,"W4.0") )



