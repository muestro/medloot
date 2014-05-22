from google.appengine.ext import ndb


# HITROLL, DAMROLL, INFLUENCE_MELEE, INFLUENCE_SPELLS, BLUNT_VULNERABILITY, SHARP_VULNERABILITY, HIT_POINTS,
# MANA, ARMOR, SAVING_SPELL, SAVING_BREATH, SAVING_ROD, INT, STR, WIS, CON, DEX
class Affect(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.IntegerProperty()

    def to_string(self):
        if self.value >= 0:
            return "\t+{0} to {1}\n".format(self.value, self.name)
        else:
            return "\t{0} to {1}\n".format(self.value, self.name)