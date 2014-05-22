from google.appengine.ext import ndb


# Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
# Level 30 spell of Resurrect.  Holds 7 charges and has 5 charges left.
class Spell(ndb.Model):
    name = ndb.StringProperty()
    level = ndb.IntegerProperty()
    charges = ndb.IntegerProperty()
    regenerates = ndb.BooleanProperty()

    def to_string(self):
        if self.regenerates:
            return "Regenerates level {0} spell of {1}. Has {2} maximum charges.\n".format(
                self.level, self.name, self.charges)
        else:
            return "Level {0} spell of {1}.  Holds {2} and has {2} charges left.\n".format(
                self.level, self.name, self.charges)