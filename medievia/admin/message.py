from google.appengine.ext import db
from google.appengine.api import users
import administrator
import datetime


class Message(db.Model):
    owner = db.StringProperty()
    message = db.StringProperty()
    date = db.DateTimeProperty()


# db CRUD ops
def log(message_string):
    if message_string is None:
        return

    admin = administrator.get(email=users.get_current_user().email())
    if admin:
        owner = admin.alias
    else:
        owner = "Admin"

    message = Message()
    message.message = message_string
    message.owner = owner
    message.date = datetime.datetime.now()
    message.put()


def get(item_key=None):
    try:
        if item_key:
            return db.get(db.Key(item_key))
        else:
            return db.GqlQuery('SELECT * FROM Message ORDER BY date DESC').run()
    except db.BadKeyError:
        return False