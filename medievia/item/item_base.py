from google.appengine.ext import ndb


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

    damage_dice1 = ndb.IntegerProperty()
    damage_dice2 = ndb.IntegerProperty()
    ac_apply = ndb.IntegerProperty()