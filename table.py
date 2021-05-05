import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

import urllib
import re
import datetime

import datastore

from google.appengine.api import users

#from google.appengine.dist import use_library
#use_library('django','1.2')


class Author(object):

  def  __init__(self,fname,lname):
    self.author = fname + " " + lname



class Template(webapp.RequestHandler):

    def get(self):

#       guestbook_name=self.request.get('guestbook_name')
#        greetings_query = Greeting.all().ancestor(
#            guestbook_key(guestbook_name)).order('-date')
#        greetings = greetings_query.fetch(10)

#       greetings = ["author":"Joe","Jack","Stacia"]
        a = Author("Ernest" , "Hemingway")
        b = Author("Mark" , "Twain")
        c = Author("John" , "Steinbeck")

        greetings = ["Joe","Jack","Stacia"]
        greetings = [ a,b,c]

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'table.html')
        self.response.out.write(template.render(path, template_values))


class Test(webapp.RequestHandler):
    def Writeln(self,t):
       self.Write(t+"\n")

    def Write(self,t ):
       self.response.out.write( t )

    def get(self):

        self.response.headers['Content-Type'] = 'text/html'

        self.Writeln('<html>\n')
        self.Writeln('<head>\n')
        self.Writeln('</head>\n')
        self.Writeln('<h1>Testing</h1>\n')


class PATCTable(webapp.RequestHandler):

    def get(self):

        a = Author("Ernest" , "Hemingway")
        b = Author("Mark" , "Twain")
        c = Author("John" , "Steinbeck")

        greetings = ["Joe","Jack","Stacia"]
        greetings = [ a,b,c]

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        club = datastore.Club.get_by_key_name('PATC')
        query = db.Query(datastore.Membership)
        query.ancestor( club.key() )
#       query.filter('year >= ' , 2011)
        query.order('last' )
        res = query.fetch( limit=300 )

        template_values = {
            'results': res,
        }

#   first,last,year, email,address,ntrp,interest

        path = os.path.join(os.path.dirname(__file__), 'table.html')
        self.response.out.write(template.render(path, template_values))



application = webapp.WSGIApplication(
                                     [('/table', PATCTable)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":

#   print __file__
#   print __name__

    main()

