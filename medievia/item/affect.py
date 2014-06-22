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

    def copy(self):
        new_affect = Affect()
        new_affect.name = self.name
        new_affect.value = self.value
        return new_affect

    def is_same_type(self, affect2):
        return self.name == affect2.name

    def is_equal(self, affect2):
        return self.name == affect2.name and \
            self.value == affect2.value


def get_better_affect(affect1, affect2):
    if affect1.name.lower().startswith("saving"):
        return affect1 if affect1.value < affect2.value else affect2
    else:
        return affect1 if affect1.value > affect2.value else affect2

def get_worse_affect(affect1, affect2):
    if affect1.name.lower().startswith("saving"):
        return affect1 if affect1.value > affect2.value else affect2
    else:
        return affect1 if affect1.value < affect2.value else affect2