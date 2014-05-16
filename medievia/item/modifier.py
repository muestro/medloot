from google.appengine.ext import ndb


class Modifier(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.IntegerProperty()
    descriptor = ndb.StringProperty()
