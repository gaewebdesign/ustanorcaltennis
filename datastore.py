from google.appengine.ext import blobstore
from google.appengine.ext import db

class OpenDate(db.Model):
  openingdate = db.DateTimeProperty()  
  currentdate = db.DateTimeProperty()  


class CourtTime(db.Model):
  id = db.IntegerProperty()
  courts = db.StringListProperty()

  date = db.DateTimeProperty()  
  start = db.DateTimeProperty()  
  end = db.DateTimeProperty()  

  desc = db.TextProperty()  
  location = db.StringProperty()

  weekday = db.StringProperty()
  owner = db.StringProperty()  


class Captain(db.Model):
  count = db.IntegerProperty()
  fname = db.StringProperty()
  lname = db.StringProperty()
  user  = db.StringProperty()
  password  = db.StringProperty()
  team  = db.StringProperty()
  courts = db.ListProperty(db.Key)



#http://www.terminally-incoherent.com/blog/2011/03/28/student-webspace-in-the-cloud-google-app-engine/

class BlobKey(db.Model):
  name = db.StringProperty()
  mykey = blobstore.BlobReferenceProperty( )
  date= db.DateProperty()

#class Player(db.Model):
class FacilityPlayer(db.Model):
  city = db.StringProperty()
  date = db.DateTimeProperty()
  facility = db.IntegerProperty()
  fname = db.StringProperty()
  gender = db.StringProperty()
  lname = db.StringProperty()
  playerid = db.IntegerProperty()
  rating = db.StringProperty()
  roster = db.StringProperty()
  teamid = db.IntegerProperty()


class FacilityRoster(db.Model):
  facility = db.IntegerProperty()
  teamid = db.IntegerProperty()
  playerid = db.IntegerProperty()
  fname = db.StringProperty()
  lname = db.StringProperty()
  roster= db.StringProperty()
  date= db.DateProperty()
  city = db.StringProperty()
  gender = db.StringProperty()
  rating = db.StringProperty()


class FacilityTeam(db.Model):
  captain = db.StringProperty()
  facility = db.IntegerProperty()
  name = db.StringProperty()
  page = db.TextProperty()
  position = db.IntegerProperty()
  teamid = db.IntegerProperty()
  updated = db.DateTimeProperty()




