from google.appengine.ext import db


class Administrator(db.Model):
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

    admin = db.get(db.Key(key))
    alias = admin.alias
    admin.delete()
    return alias


def get(item_key=None, email=None):
    try:
        if item_key:
            return db.get(db.Key(item_key))
        elif email:
            return db.GqlQuery('SELECT * FROM Administrator WHERE email = :1', email.lower()).get()
        else:
            return db.GqlQuery('SELECT * FROM Administrator ORDER BY alias').run()
    except db.BadKeyError:
        return False


def is_admin(email):
    admins = get()
    for admin in admins:
        if admin.email.lower() == email.lower():
            return True

    return False