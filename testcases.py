
import webapp2  # (NEWSESSION)

import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

import urllib
import re,cgi,calendar,string,types,random
import datetime

import datastore,library

from google.appengine.api import users

import mysession # (NEWSESSION)

def monday( m,d, y):
   return datetime.date(m,d,y) - datetime.timedelta( datetime.date(m,d,y).weekday())


class Days(object):
  def __init__(self,d):
     self.day = d
     self.selected = ""

class Months(object):
  def __init__(self,n,m):
     self.number = n
     self.month = m


class TestcaseHandler( mysession.BaseHandler )

    def Write(self,t):
     self.response.out.write(t)

    def Writeln(self,t):
     self.response.out.write(t)
     self.response.out.write("<br>")


    def FillReservation(self):

      query="select __key__ from Captain order by lname"
      keys =  db.GqlQuery( query)
      captains = db.get(keys)
      captainlist = []
      for e in captains:
            keyname =  e.key().name() 
            self.Writeln(" owner = " + str(keyname) )
            captainlist.append( keyname )

      x  = random.randrange(0, 30)% len(captainlist)

      query="select __key__ from CourtTime"
      keys =  db.GqlQuery( query)
      courts = db.get(keys)
      reservelist=[]
      for  e in courts:
         if( type( e.owner) is types.NoneType ):
             x  = random.randrange(0, 30)% len(captainlist)
             e.owner =  captainlist[x]
             self.Writeln(" set owner to " + str( captainlist[x]) )
             reservelist.append( e)

# Increment count for captain
             user = datastore.Captain.get_by_key_name( e.owner )
             user.count = user.count+1
             db.put( user )             

      db.put( reservelist )

    def PartialReservation(self):

      query="select __key__ from Captain order by lname"
      keys =  db.GqlQuery( query)
      captains = db.get(keys)
      captainlist = []
      for e in captains:
            keyname =  e.key().name() 
            self.Writeln(" owner = " + str(keyname) )
            captainlist.append( keyname )

      x  = random.randrange(0, 30)% len(captainlist)

      query="select __key__ from CourtTime"
      keys =  db.GqlQuery( query)
      courts = db.get(keys)
      reservelist=[]

      self.Writeln(  len(courts) )
      lc =  len(courts) 

      for  i in range(0,lc/2):
         p  = random.randrange(0, lc)% lc
         e = courts[p]

         if( type( e.owner) is types.NoneType ):
             x  = random.randrange(0, 30)% len(captainlist)
             e.owner =  captainlist[x]
             self.Writeln(" set owner to " + str( captainlist[x]) )
             reservelist.append( e)

# Increment count for captain
             user = datastore.Captain.get_by_key_name( e.owner )
             user.count = user.count+1
             db.put( user )             

      db.put( reservelist )


    def get(self,testcase):

        if( testcase == "all"):
         self.FillReservation()
        elif( testcase == "partial"):
         self.PartialReservation()
        else:
         self.Writeln("none")

app = webapp2.WSGIApplication(
             [('/(all)', TestcaseHandler ),
             ('/(partial)', TestcaseHandler )
          ], debug=True , config=mysession.config)



