from google.appengine.ext import ndb
import medievia.item.spell
import medievia.item.focus


class ItemBase(ndb.Model):
    name = ndb.StringProperty()
    keywords = ndb.StringProperty(repeated=True)

    # ARMOR, WEAPON, WORN, WAND, TREASURE, TRASH, STAFF, SCROLL, MAGIC, NOTE, OTHER, REGEN, BOAT, CONTAINER, LIGHT
    item_type = ndb.StringProperty(repeated=True)

    # ANTI-GOOD(...), ANTI-MAGE(...), ATTACK, BLESS, BONDS, CLAN, CLANLOCK, COLD, DONATION, EVIL, FIRE, GLOW, HOLY, HUM
    effects = ndb.StringProperty(repeated=True)

    # ABOUT, ARMS, BODY, FEET, FINGER, HANDS, HEAD, HIP, HOLD, LEGS, NECK, SHIELD, TAKE, THROW, WAIST, WIELD, WRIST
    equipable_locations = ndb.StringProperty(repeated=True)

    weight = ndb.IntegerProperty()
    value = ndb.IntegerProperty()
    level_restriction = ndb.IntegerProperty()
    available_weight = ndb.IntegerProperty()

    # Class Restrictions: ANTI_MAGE ANTI_CLERIC ANTI_WARRIOR ANTI_THIEF
    class_restrictions = ndb.StringProperty(repeated=True)

    # ANTI_CLERIC, ANTI_MAGE, ANTI_THIEF, ANTI_WARRIOR, BACKSTABBER, DAGGER, LONG, None, TWO_HANDED
    attributes = ndb.StringProperty(repeated=True)

    # Regenerates level 26 spell of Bloodbath.  Has 1 maximum charges.
    # Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
    spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)

    damage_dice1 = ndb.IntegerProperty()
    damage_dice2 = ndb.IntegerProperty()
    missile_damage = ndb.FloatProperty()

    ac_apply = ndb.IntegerProperty()
    focus = ndb.StructuredProperty(medievia.item.focus.Focus, repeated=True)

    def is_anti_mage(self):
        return "ANTI_MAGE" in self.attributes or "ANTI_MAGE" in self.class_restrictions

    def is_anti_cleric(self):
        return "ANTI_CLERIC" in self.attributes or "ANTI_CLERIC" in self.class_restrictions

    def is_anti_warrior(self):
        return "ANTI_WARRIOR" in self.attributes or "ANTI_WARRIOR" in self.class_restrictions

    def is_anti_thief(self):
        return "ANTI_THIEF" in self.attributes or "ANTI_THIEF" in self.class_restrictions


# used when creating an item summary from a standard item.  Make sure all attributes in this class are copied over.
def copy_attributes(from_item, to_item):
    # try to copy all of the properties from ItemBase to the passed in object
    to_item.name = from_item.name
    to_item.keywords = from_item.keywords
    to_item.item_type = from_item.item_type
    to_item.effects = from_item.effects
    to_item.equipable_locations = from_item.equipable_locations
    to_item.weight = from_item.weight
    to_item.value = from_item.value
    to_item.level_restriction = from_item.level_restriction
    to_item.available_weight = from_item.available_weight
    to_item.class_restrictions = from_item.class_restrictions
    to_item.attributes = from_item.attributes
    to_item.damage_dice1 = from_item.damage_dice1
    to_item.damage_dice2 = from_item.damage_dice2
    to_item.ac_apply = from_item.ac_apply
    to_item.spells = from_item.spells

