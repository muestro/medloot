from google.appengine.ext import db
import administrator
import datetime


class Message(db.Model):
    owner = db.ReferenceProperty(administrator.Administrator)
    message = db.StringProperty()
    date = db.DateTimeProperty()


# db CRUD ops
def log(admin, message_string):
    if message_string is None:
        return

    message = Message()
    message.message = message_string
    message.owner = admin
    message.date = datetime.datetime.now()
    message.put()


def get(item_key=None):
    try:
        if item_key:
            return db.get(db.Key(item_key))

        else:
            return db.GqlQuery('SELECT * FROM Message ORDER BY alias').run()
    except db.BadKeyError:
        return False