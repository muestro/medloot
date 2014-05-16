from google.appengine.ext import ndb

import medievia.item.modifier


class ItemSummary(ndb.Model):

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
    days_left = ndb.IntegerProperty()

    # The object appears to be in perfect pristine condition.
    # The object appears to be in excellent condition.
    # The object appears to be in good condition.
    # The object appears to be in fair condition.
    # The object looks as if it will fall apart any day now.
    condition = ndb.StringProperty()

    # Class Restrictions: ANTI_MAGE ANTI_CLERIC ANTI_WARRIOR ANTI_THIEF
    class_restrictions = ndb.StringProperty(repeated=True)

    # +X% to parry/rage/disarm/X-Heal/Hammer of Faith/Demonfire/Harm (success/efficiency/proficiency)
    modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)

    # ANTI_CLERIC, ANTI_MAGE, ANTI_THIEF, ANTI_WARRIOR, BACKSTABBER, DAGGER, LONG, None, TWO_HANDED
    attributes = ndb.StringProperty(repeated=True)

    damage_dice1 = ndb.IntegerProperty()
    damage_dice2 = ndb.IntegerProperty()
    ac_apply = ndb.IntegerProperty()
    charges = ndb.IntegerProperty()

    # affects
    hitroll = db.IntegerProperty()
    damroll = db.IntegerProperty()
    hit_points = db.IntegerProperty()
    mana = db.IntegerProperty()
    armor = db.IntegerProperty()
    saving_spell = db.IntegerProperty()
    saving_breath = db.IntegerProperty()
    saving_rod = db.IntegerProperty()
    int = db.IntegerProperty()
    str = db.IntegerProperty()
    wis = db.IntegerProperty()
    con = db.IntegerProperty()
    dex = db.IntegerProperty()
    influence_melee = db.IntegerProperty()
    influence_spells = db.IntegerProperty()
    blunt_vulnerability = db.IntegerProperty()
    sharp_vulnerability = db.IntegerProperty()


def create_or_update(item):
    raw_item = ItemSummary()

    #just manually copy each property over :P


    raw_item.put()
