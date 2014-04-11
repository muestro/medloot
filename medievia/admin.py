from google.appengine.ext import db


class Admin(db.Model):
    email = db.StringProperty()
    alias = db.StringProperty()


# db CRUD ops
def create_or_update(admin):
    if admin is None:
        return

    admin.put()


def delete(key):
    if key is None:
        return

    item = db.get(db.Key(key))
    item.delete()


def get(item_key=None):
    try:
        if item_key:
            return db.get(db.Key(item_key))

        else:
            return db.GqlQuery('SELECT * FROM Admin ORDER BY alias').run()
    except db.BadKeyError:
        return False


def is_admin(email):
    admins = get()
    for admin in admins:
        if admin.email.lower() == email.lower():
            return True

    return False