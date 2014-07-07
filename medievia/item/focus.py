from google.appengine.ext import ndb


# Focus for: Malediction
class Focus(ndb.Model):
    name = ndb.StringProperty()
    strength = ndb.StringProperty()

    def to_string(self):
        return "Focus for: {0}\n".format(self.name) + "Strength: {0}\n".format(self.strength)
