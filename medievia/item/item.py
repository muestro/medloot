from google.appengine.ext import ndb
import medievia.item.modifier
import medievia.item.spell
import medievia.item.affect
import hashlib


# model object
# noinspection PyTypeChecker
class Item(ndb.Model):
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
    spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)

    # affects
    affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)

    is_expired = ndb.BooleanProperty()

    source_string = ''

    def is_populated(self):
        return property_has_value(self.name) and property_has_value(self.keywords) \
            and property_has_value(self.item_type)

    def to_string(self):
        # object, name, keywords
        output = "Object: {0} [{1}]\n".format(self.name, " ".join(self.keywords))

        # item type, effects
        output = output + "Item Type: {0} \tEffects: {1}\n".format(" ".join(self.item_type), " ".join(self.effects))

        # equipable locations
        output = output + "Equipable Location(s): {0}\n".format(" ".join(self.equipable_locations))

        # weight, value, level restriction
        output = output + "Weight: {0} \tValue: {1} \tLevel Restriction: {2}\n".format(self.weight, self.value,
                                                                                       self.level_restriction)
        # condition
        if self.condition:
            output = output + self.condition + "\n"

        # days left
        if self.days_left:
            if self.days_left == -1:
                output = output + "Days Left: Infinity\n"
            else:
                output = output + "Days Left: {0}\n".format(self.days_left)


        # ac-apply
        if self.ac_apply:
            output = output + "AC-apply of {0}\n".format(self.ac_apply)

        # attributes
        if self.attributes:
            output = output + "Attributes: {0}\n".format(" ".join(self.attributes))

        # damage dice
        if self.damage_dice1 and self.damage_dice2:
            output = output + "Damage Dice of {0}d{1}\n".format(self.damage_dice1, self.damage_dice2)

        # spells
        if self.spells:
            for spell in self.spells:
                output = output + spell.to_string()

        # class restrictions
        if self.class_restrictions:
            output = output + "Class Restrictions: {0}\n".format(" ".join(self.class_restrictions))

        # affects
        if self.affects:
            if self.affects > 0:
                output = output + "Affects:\n"
            for affect in self.affects:
                output = output + affect.to_string()

        # modifiers
        if self.modifiers and self.modifiers > 0:
            output = output + "Skill/Spell Modifiers: \n"
            for modifier in self.modifiers:
                output = output + modifier.to_string()

        return output


def property_has_value(prop):
    return isinstance(prop, basestring) or isinstance(prop, list)


# db CRUD ops
def create_or_update_item(item):
    if item is None:
        return
    item.put()

    # update the corresponding item_info
    #_update_item_info(item)


def delete_item(key):
    if key is None:
        return
    key.delete()


def get_items(name=None):
    if name is not None:
        items = ndb.gql('SELECT * FROM Item WHERE name = :1', name).run()
    else:
        items = ndb.gql('SELECT * FROM Item').run()
    return items


def get_item_count():
    q = Item.query()
    return q.count()


def get_item(item_key):
    item = item_key.get()
    return item


def get_key_name(name, affect_strings):
    if affect_strings and len(affect_strings) > 0:
        affect_strings.sort()
        hash_string = name + "|" + "|".join(affect_strings)
    else:
        hash_string = name
    return hashlib.md5(hash_string).hexdigest()


def _update_item_info(item):
    # get all the items from the datastore that share the same name
    items = get_items(item.name)

    affect_min = {}
    affect_max = {}
    affect_base = {}

    # gather the min/max/base stats
    for item in items:
        for affect in item.affects:
            value = int(affect.split()[0])
            name = affect.split()[2]

            if name not in affect_min:
                affect_min[name] = value
                affect_max[name] = value
            else:
                if value < affect_min[name]:
                    affect_min[name] = value

                if value > affect_max[name]:
                    affect_max[name] = value

            # check base
            if item.is_expired:
                if name not in affect_base:
                    affect_base[name] = value
                else:
                    if value > affect_base[name]:
                        affect_base[name] = value

    # update item_info
