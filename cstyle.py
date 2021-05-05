from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.webapp import template

import os,re,datetime,sys


class MainHandler(webapp.RequestHandler):
    def __init__(self):
        pass

    def Writeln(self,t):
        self.response.out.write(t)

    def css(self ):
        template_values = {
#            'greetings': greetings,
#            'url': url,
#            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'css.html')
        self.response.out.write(template.render(path, template_values))


    def get(self ):

        self.Writeln('</html>')



def main():
    application = webapp.WSGIApplication(
          [  ('/cstyle', MainHandler),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
  main()

