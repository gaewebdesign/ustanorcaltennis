import webapp2

from google.appengine.api import urlfetch

from google.appengine.ext import db
from google.appengine.ext import ndb


from datetime import timedelta

import urllib,re,datetime,string,sys,os

import json

from webapp2_extras import  sessions


def Writeln( selfobj, *t):
   for x in t:
     selfobj.response.out.write(x )
     selfobj.response.out.write(" ")

   selfobj.response.out.write("<br>")

def Write( selfobj, *t):
   for x in t:
     selfobj.response.out.write(x )
     selfobj.response.out.write(" ")


class BaseHandler(webapp2.RequestHandler):
  def dispatch( self ):
    self.session_store = sessions.get_store(request=self.request)

    try:
      # Dispatch the request
      webapp2.RequestHandler.dispatch(self)
    finally:
      #Save all sessions
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session( self ):
      #return a session using the default cookie key
      return self.session_store.get_session()


class MainHandler( BaseHandler ):

    def get(self):
       user = self.session.get('user')

       if user:
         self.response.write('Session has this value: %r.' % user)
         self.session['user']='okamoto'
       else:
         self.session['user'] = 'roger'
         self.response.write('Session is empty .')



config = {}
config['webapp2_extras.sessions'] = {'secret_key' :  'superman' }


app = webapp2.WSGIApplication(
                                     [
                                      ('/', MainHandler),
                                     ],
                                     debug=True,
                                     config=config)




