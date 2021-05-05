from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import os, urllib,re,datetime
import datastore
import library

class MainHandler(webapp.RequestHandler):
    def __init__(self):
#      g =  datastore.TournyPlayer.get_or_insert( key_id)
        patc = datastore.Club.get_or_insert("PATC")
        patc.name = "Palo Alto Tennis Club"
        patc.id = 72
        patc.year = 2011
        patc.put()

        sctc = datastore.Club.get_or_insert("SCTC")
        sctc.name = "Santa Clara Tennis Club"
        sctc.id = 3483
        sctc.year = 2011
        sctc.put()

        stc = datastore.Club.get_or_insert("STC")
        stc.name = "Sunnyvale Tennis Club"
        stc.id = 463
        stc.year = 2011
#       stc.date  = str(datetime.date.today())
        stc.put()


    def Writeln(self,data):
        self.response.out.write(data+"<br>")

    def Write(self,data):
        self.response.out.write(data+"\n")

    def post(self,url):


        if( re.search('patc', url, re.IGNORECASE)):
          self.savepatc(url)
        elif( re.search('sctc', url, re.IGNORECASE)):
          self.savesctc(url)


    def savesctc(self,url):
        self.Writeln('url = ' + url)
        blob_key =  self.request.get('theBlob')
        self.Writeln('theBlob =' + blob_key)
        club = datastore.Club.get_by_key_name('SCTC')

        query = 'select __key__ from Membership '
        keys =  db.GqlQuery( query )
        for k in keys:
         t = db.get(k)
         t.delete()

        blob_reader = blobstore.BlobReader(blob_key)
        playerlist= []                           # List to hold members
        regphone = re.compile("([\d]*)-([\d]*)-([\d]*)",re.IGNORECASE )

        for line in blob_reader:
           if( re.match("Last",line)): continue

           u = line.rsplit(",")                  # Split the line delimited by ,
           r = [ n.strip(" \r\n") for n in u ]   # Strip out end whitepace (includes \r\n )

           if( len(r) < 3): continue
           last = r[0]
           first = r[1]
           city = r[2]
           zip = r[3]
           rating = r[6]
           hphone = r[4]
           wphone = r[5]

#          Membership Year (encoded via * or #)
           year = "2011"
           if(re.search("#",last)): year  = "2012"

#          Last name ( strip out *#)
           last = last.strip("*#")

#          City (fix up Santa Clara errors )
           if(re.search("clara",city,re.IGNORECASE)): city = "Santa Clara"

#          Add .0 to rating if necessary
           rating = rating.strip(" ")
           if(len(rating) == 1): rating  = rating+".0"

#          Fix phone (unlikely)
#          mhome = regphone.findall( hphone )
#          mwork = regphone.findall( wphone )

           print( first, last,city,zip,hphone,wphone,rating,year )
           g = datastore.Membership( key_name= first+"_"+last ,parent=club.key() )
           g.first = first
           g.last = last
           g.year = int(year)
           g.email = ""
           g.city = city
           g.zip = zip
           g.rating = rating
           playerlist.append( g )


#       Put everyone in at the same time
        db.put( playerlist )

    def savepatc(self,url):
        self.Writeln('read post ' + url)
        blob_key =  self.request.get('theBlob')
        self.Writeln('theBlob =' + blob_key)

        blob_reader = blobstore.BlobReader(blob_key)
        club = datastore.Club.get_by_key_name('PATC')
        id = club.id
        playerlist= []         # List to hold members

        curr_keys =  db.GqlQuery( 'select __key__ from Membership'  )
        self.Writeln("current members = " + str( curr_keys.count() ))


#       Read the blob, parse and save into DB 
        blob_reader.readline()                     # Skip the first line (header information)
        for line in blob_reader:
             u = line.rsplit(",")                  # Split the line delimited by ,
             r = [ n.strip(" \r\n") for n in u ]   # Strip out end whitepace (includes \r\n )


             if( len(line) < 2): continue
             if( int(r[2]) < club.year): continue


             key = r[0]+"_"+r[1]+"_"+r[3]+"@"+r[4]

             g = datastore.Membership( key_name=key ,parent = club.key() )
             g.first = r[0]
             g.last = r[1]
             g.year = int(r[2])    #read as string, but stored at int

             g.email = ""
             if( len(r[3])>2 and len(r[4])>2):
                g.email = r[3] + "@" + r[4]


             g.address=""
             if( len(r[5]) and len(r[6]) and len(r[7]) and len(r[8]) ):
                g.address = r[5]+","+r[6]+ ","+r[7]+","+r[8]


             g.phone = ""
             if( len(r[9])==3 and len(r[10])==8):  g.phone = r[9] + " " + r[10]

             rating = r[12]
             rating = rating.strip(" ")
             if(len(rating) == 1): rating  = rating+".0"
             g.ntrp = r[11]+rating
   
# D(ropin),S(ocial),C(linic),L(adder),B(oard,N(ewsletter)
             g.interest = ""

             if( len(r[13])>0 ):          g.interest += "n"
             if( len(r[14])>0 ):          g.interest += "*"

#            lower case for interested in
             if( re.search('dro',r[15] , re.IGNORECASE)):   g.interest += "d"
             if( re.search('tou',r[15] , re.IGNORECASE)):   g.interest += "s"
             if( re.search('soc',r[15] , re.IGNORECASE)):   g.interest += "s"
             if( re.search('cli',r[15] , re.IGNORECASE)):   g.interest += "c"
             if( re.search('lad',r[15] , re.IGNORECASE)):   g.interest += "l"
             if( re.search('boa',r[15] , re.IGNORECASE)):   g.interest += "b"

#            UPPER CASE for willing to help
             if( re.search('dro',r[16] , re.IGNORECASE)):   g.interest += "D"
             if( re.search('tou',r[16] , re.IGNORECASE)):   g.interest += "S"
             if( re.search('soc',r[16] , re.IGNORECASE)):   g.interest += "S"
             if( re.search('cli',r[16] , re.IGNORECASE)):   g.interest += "C"
             if( re.search('lad',r[16] , re.IGNORECASE)):   g.interest += "L"
             if( re.search('boa',r[16] , re.IGNORECASE)):   g.interest += "B"
             if( re.search('new',r[16] , re.IGNORECASE)):   g.interest += "N"

             playerlist.append( g )

#       Clean out current members
        self.Writeln("wipe out " + club.name)
        for k in curr_keys:
         t = db.get(k)
         t.delete()

#       Then put in new ones
        self.Writeln("put "+ club.name )
        for p in playerlist:
          self.Writeln(p.first+' '+p.last+' ' + p.ntrp +' '+ str(p.year) +' ' +p.interest )   

        db.put( playerlist )

#       Done if there's no Copy
        _copy =  db.GqlQuery( 'select __key__ from _Copy' )
        if( _copy.count()==0): 
          self.Writeln("Finished, no previous _Copy" )
          return
        else:
          self.Writeln("Checking for new members" )


#       Check if new
        keys =  db.GqlQuery( 'select __key__ from _NewMember')
        for k in keys:
         t = db.get(k)
         t.delete()

        self.Writeln( "New members " )
        _copied = datastore._Copy.get_or_insert("players")

        for p in playerlist:
           key = p.first+"_"+p.last+"_"+p.email
           if( not key in _copied.keys):
             h = datastore._NewMember( key_name=key ,parent=club.key()  )
             h.first = p.first
             h.last = p.last
             h.ntrp = p.ntrp
             h.year = p.year
             h.email = p.email
             self.Writeln( "add "+ key + ' ' + h.first +  ' ' + h.last +' ' + h.email)
             h.put()

        return


#    This old method 
        for p in playerlist:
           key = p.first+"_"+p.last+"_"+p.email
           m = datastore._Membership.get_by_key_name(key ,parent=club.key() )
           if (  m == None):      
                h = datastore._NewMember( key_name=key ,parent=club.key()  )
                h.first = p.first
                h.last = p.last
                h.ntrp = p.ntrp
                h.email = p.email
                self.Writeln( "add "+ key + ' ' + h.first +  ' ' + h.last +' ' + h.email)
                h.put()


    def get(self,url):
        filter=""
        if( re.search('patc',url,re.IGNORECASE) ):
         club = datastore.Club.get_by_key_name('PATC')
         filter="patc"
        elif( re.search('sctc', url,re.IGNORECASE )):
         club = datastore.Club.get_by_key_name('SCTC')
         filter="sctc"
        elif( re.search('lp',url,re.IGNORECASE)):
         club = datastore.Club.get_by_key_name('STC')
         filter="stc"

        self.Write('<html>')
        self.Write('<body>')
        self.Write('<title>'+ club.name + '</title>')
        self.Write('<h1>'+ club.name + '</h1>')

        upload_url = blobstore.create_upload_url('/upload')
        self.Write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.Write("""Upload Membership File: <input type="file" name="file"><br>""")
        self.Write(""" <input type="Submit" name="submit" value="Submit"> </form></body></html>""")

        chk = " checked "
        theBlob = ""
        self.response.out.write('<form method="POST" >')
        for b in blobstore.BlobInfo.gql("order by creation desc"):

          if( re.search(filter, b.filename, re.IGNORECASE) == None): continue

          day = re.match( "([\d]{4}-[\d]{1,2}-[\d]{1,2})" , str(b.creation) )
          hr = re.search( "([\d]{2}:[\d]{2}:[\d]{2})" , str(b.creation) )
          date = day.group(0) + " " + hr.group(0)
          sel = "theBlob"
          fn = b.filename
          theBlob = str(b.key())
          creation = b.creation
          self.Write('<input type=radio'+chk+' name="'+sel+'" value="'+theBlob+'">'+ fn+" " + date + ' <br>')
          chk = ""

        self.Writeln("""Select Membership File to read: <br><input type="Submit" value="Read" name="blob" ><br>""")
        self.response.out.write('</form>')


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
     
        self.response.out.write('posted')

#       upload_files = self.get_uploads('file')
#       blob_info = upload_files[0]
#       ikey=blob_info.key()

        u = "SCTC"
#        g = datastore.BlobKey(key_name = u )
#        g.name  = "SCTCMembership"
#       g.mykey = blob_info.key()
#        g.put()

#       self.redirect('/up')  # 10/13/11

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blob_key):
       blob_key = str(urllib.unquote(blob_key))
 
       if not blobstore.get(blob_key):
            self.error(404)
       else:
            self.send_blob(blobstore.BlobInfo.get(blob_key), save_as=True)


class BlobReader( webapp.RequestHandler):
   def get(self):

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("reader <br>")

        blob = blobstore.BlobInfo.all()
        blob = blobstore.BlobInfo.gql("order by creation")

        self.response.out.write("len = "+ str(len(blob)))
        
        b = blob[1]      
        blob_key = b.key()

        blob_reader = blobstore.BlobReader(blob_key)

#        for line in blob_reader:
#             print("-"+line )



def main():
    application = webapp.WSGIApplication(
          [  ('/(loadpatc)', MainHandler),
           ('/(loadsctc)', MainHandler),
           ('/(loadctc)', MainHandler),
           ('/(loadlp)', MainHandler),
           ('/upload', UploadHandler),
           ('/reader', BlobReader),
           ('/serve/([^/]+)?', ServeHandler),
           ('/[ \d\w\/]*', UploadHandler),
          ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
  main()

