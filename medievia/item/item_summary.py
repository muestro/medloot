from google.appengine.ext import ndb

import medievia.item.modifier
import medievia.item.spell


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

    # Regenerates level 26 spell of Bloodbath.  Has 1 maximum charges.
    # Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
    # Level 30 spell of Resurrect.  Holds 7 charges and has 5 charges left.
    spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)

    # affects
    hitroll = ndb.IntegerProperty()
    damroll = ndb.IntegerProperty()
    hit_points = ndb.IntegerProperty()
    mana = ndb.IntegerProperty()
    armor = ndb.IntegerProperty()
    saving_spell = ndb.IntegerProperty()
    saving_breath = ndb.IntegerProperty()
    saving_rod = ndb.IntegerProperty()
    int = ndb.IntegerProperty()
    str = ndb.IntegerProperty()
    wis = ndb.IntegerProperty()
    con = ndb.IntegerProperty()
    dex = ndb.IntegerProperty()

    # +1 to INFLUENCE_MELEE
    influence_melee = ndb.IntegerProperty()
    influence_spells = ndb.IntegerProperty()
    blunt_vulnerability = ndb.IntegerProperty()
    sharp_vulnerability = ndb.IntegerProperty()


def create_or_update(item):
    raw_item = ItemSummary()

    #just manually copy each property over :P


    raw_item.put()
