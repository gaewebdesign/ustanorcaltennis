import webapp2   # (NEWSESSION)

#from google.appengine.ext import webapp  (NEWSESSION)


from google.appengine.ext.webapp.util import run_wsgi_app
import datetime,re


class MainHandler(webapp2.RequestHandler):
#  def __init__(self):
#    pass

  def get(self ):

# http://vancouver-webpages.com/META/FAQ.html#redirect

# http://code.google.com/appengine/docs/python/tools/webapp/redirects.html

    today = datetime.datetime.date(datetime.datetime.now())
    current = re.split('-', str(today)) 
    month = current[1]
    year  = current[0]

#    print("date: "+ str(month) +"/" +  str(year))

#    self.response.out.write("go")

    self.redirect("/month/"+ month + "/" + year )



#def main():
#    application = webapp.WSGIApplication(
#          [ ('/', MainHandler)
#          ], debug=True)
#    run_wsgi_app(application)

#if __name__ == '__main__':
#  main()


app = webapp2.WSGIApplication(
          [ ('/', MainHandler)
          ], debug=True)

