import webapp2  # (NEWSESSION)
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template
from google.appengine.ext import db

import os,re,datetime,sys, calendar,cgi,types

import datastore,library

#from appengine_utilities.sessions import Session # (NEWSESSION)

# http://www.fiveriversyoga.com/a-dedicated-life-practice

import mysession # (NEWSESSION)

class Courts:
   weekday=""            # day of week
   date=""               # date of reservation

   courts=""             # courts (string)
   location=""           # LP or Mango
   start=""              # start time   (converted to am/pm)
   end=""                # end time     (converted to am/pm)
   desc=""               # description  

# used in DelCourt nfirmHandler?
   date=""               # description  
   key=""                # db key


class DelConfirmHandler( mysession.BaseHandler):
    def post(self ):
      print("DelConfirmHandler")
      courtlist = []
      try:
        keylist = self.request.get_all('keys')
        print("get keys")
        for key in keylist:
            print(key)

            p = db.get(key)   #Get the court by its unique key (key)
            print("db.get(key)")
            continue
            c = Courts()
            c.date = library.cday(p.start)                   
            c.weekday = p.weekday
            c.start = library.ctime(p.start)                   
            c.end = library.ctime(p.end)                   
            c.desc = p.desc
            c.courts   = library.listconv( p.courts) 
            c.location = library.location(p.location)

            c.key = key
            courtlist.append(c)

      except Exception as e:
        print "EXCEPTION: " + str(e)

# weekday, date, courts,location,start,desc

      template_values = {
                "CourtList": courtlist

      }


#      path = os.path.join(os.path.dirname(__file__), 'templates','delcourtconfirm.html')
#      self.response.out.write(template.render(path, template_values))


class DelHandler( mysession.BaseHandler):
    def post(self ):
        print("post")

    def post(self):
      print("DelHandler")
      courtlist = []
      try:
        keylist = self.request.get_all('key')
        print("get keys")
        for key in keylist:
            c = Courts()
#           c.key = key
#
            p = db.get(key)   #Get the court by its unique key (key)
            print("db.get(key)")
            c.date = library.cday(p.start)                   
            c.weekday = p.weekday
            c.start = library.ctime(p.start)                   
            c.end = library.ctime(p.end)                   
            c.desc = p.desc
            c.courts   = library.listconv( p.courts) 
            c.location = library.location(p.location)

            c.key = key
            courtlist.append(c)

            print key

# DELETE  FROM DATABASE
            try:
               p.delete()
               c.desc = "Deleted"
               print("successfully deleted ")
            except:
               print "DELETION EXCEPTION"
# DELETE FROM DATABASE

      except:
        print "EXCEPTION"

# weekday, date, courts,location,start,desc

      template_values = {
                "CourtList": courtlist

      }


      path = os.path.join(os.path.dirname(__file__), 'templates','alldelcourt.html')
      self.response.out.write(template.render(path, template_values))



class ModifyHandler( mysession.BaseHandler):

    def get(self ):
      
        print("get")
        query="select __key__ from CourtTime order by date"
        keys =  db.GqlQuery( query)

        courtlist = []
        for k in keys:
           p = db.get(k)

           c = Courts()
           c.weekday = p.weekday
           c.date = library.cday(p.date)
           c.start = library.ctime(p.start)
           c.end = library.ctime(p.end)
           c.courts = library.listconv(p.courts)
           c.location = library.location(p.location)
           c.desc = p.desc
           c.key = k
           courtlist.append( c)
           print(c.date)

        template_values = {
             'CourtList' : courtlist
            }


        path = os.path.join(os.path.dirname(__file__), 'templates','all.html')
        self.response.out.write(template.render(path, template_values))

class DelConfirmHandler( mysession.BaseHandler):

    def post(self ):
      courtlist = []
      try:
        keylist = self.request.get_all('keys')
        print("get keys")
        for key in keylist:
            c = Courts()
#           c.key = key
#
            p = db.get(key)   #Get the court by its unique key (key)
            print("db.get(key)")
            c.date = library.cday(p.start)                   
            c.weekday = p.weekday
            c.start = library.ctime(p.start)                   
            c.end = library.ctime(p.end)                   
            c.desc = p.desc
            c.courts   = library.listconv( p.courts) 
            c.location = library.location(p.location)

            c.key = key
            courtlist.append(c)

            print key
      except:
        print "EXCEPTION"

# weekday, date, courts,location,start,desc

      template_values = {
                "CourtList": courtlist

      }


      path = os.path.join(os.path.dirname(__file__), 'templates','allconfirm.html')
      self.response.out.write(template.render(path, template_values))




app = webapp2.WSGIApplication(
          [  ('/all', ModifyHandler),
             ('/alldelconfirm', DelConfirmHandler),
             ('/alldel', DelHandler)

          ], debug=True , config=mysession.config)

