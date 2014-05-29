from google.appengine.ext import ndb


# Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
# Level 30 spell of Resurrect.  Holds 7 charges and has 5 charges left.
# If eaten, this will produce the effects of the Remove Poison spell.
class Spell(ndb.Model):
    name = ndb.StringProperty()
    level = ndb.IntegerProperty()
    charges = ndb.IntegerProperty()
    regenerates = ndb.BooleanProperty()
    eaten = ndb.BooleanProperty()

    def to_string(self):
        if self.regenerates:
            return "Regenerates level {0} spell of {1}. Has {2} maximum charges.\n".format(
                self.level, self.name, self.charges)
        elif self.eaten:
            return "If eaten, this will produce the effects of the {0} spell.\n".format(self.name)
        else:
            return "Level {0} spell of {1}.  Holds {2} and has {2} charges left.\n".format(
                self.level, self.name, self.charges)