from google.appengine.ext import ndb


# Skill/Spell Modifiers:
#    -4% to disarm (success)
class Modifier(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.IntegerProperty()
    descriptor = ndb.StringProperty()

    def to_string(self):
        if self.value >= 0:
            return "\t+{0}% to {1} ({2})\n".format(self.value, self.name, self.descriptor)
        else:
            return "\t{0}% to {1} ({2})\n".format(self.value, self.name, self.descriptor)

    def copy(self):
        return Modifier(name=self.name, value=self.value, descriptor=self.descriptor)

    def is_same_type(self, modifier2):
        return self.name == modifier2.name and \
            self.descriptor == modifier2.descriptor

    def is_equal(self, modifier2):
        return self.name == modifier2.name and \
            self.descriptor == modifier2.descriptor and \
            self.value == modifier2.value

    def display_name(self):
        return "{0} ({1})".format(self.name, self.descriptor)