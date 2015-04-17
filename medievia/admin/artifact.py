from google.appengine.ext import db
from google.appengine.ext import ndb


class Artifact(ndb.Model):
    def validate(self, value):
        return value[0:10000]

    value = ndb.TextProperty(validator=validate)
    submitter = ndb.StringProperty()


def get(item_key):
    try:
        return ndb.Key(urlsafe=item_key).get()

    except db.BadKeyError:
        return False