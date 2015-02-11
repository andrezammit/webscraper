from google.appengine.ext import db

class SongEntry(db.Model):
  artist = db.StringProperty(required=True)
  track = db.StringProperty(required=True)
  date = db.DateTimeProperty(required=False)