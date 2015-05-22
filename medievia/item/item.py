from google.appengine.ext import ndb
import medievia.item.item_base
import medievia.item.modifier
import medievia.item.spell
import medievia.item.affect
import hashlib


# model object
# noinspection PyTypeChecker
class Item(medievia.item.item_base.ItemBase):
    summary_item_key = ndb.KeyProperty()

    days_left = ndb.IntegerProperty()

    # The object appears to be in perfect pristine condition.
    # The object appears to be in excellent condition.
    # The object appears to be in good condition.
    # The object appears to be in fair condition.
    # The object looks as if it will fall apart any day now.
    condition = ndb.StringProperty()

    # +X% to parry/rage/disarm/X-Heal/Hammer of Faith/Demonfire/Harm (success/efficiency/proficiency)
    modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)

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
        if self.days_left is not None:
            if self.days_left == -1:
                output = output + "Days Left: Infinity\n"
            else:
                output = output + "Days Left: {0}\n".format(self.days_left)

        # focus
        if self.focus is not None:
            for focus in self.focus:
                output = output + focus.to_string()

        if self.available_weight is not None:
            output = output + "Available Weight: {0} stones\n".format(self.available_weight)

        # ac-apply
        if self.ac_apply is not None:
            output = output + "AC-apply of {0}\n".format(self.ac_apply)

        # attributes
        if self.attributes:
            output = output + "Attributes: {0}\n".format(" ".join(self.attributes))

        # class restrictions
        if self.class_restrictions:
            output = output + "Class Restrictions: {0}\n".format(" ".join(self.class_restrictions))

        # damage dice
        if self.damage_dice1 is not None and self.damage_dice2 is not None:
            if self.missile_damage is None:
                output = output + "Damage Dice of {0}d{1}\n".format(self.damage_dice1, self.damage_dice2)
            else:
                output = output + "Damage Dice of {0}d{1} and modifies missile damage by {2}\n"\
                    .format(self.damage_dice1, self.damage_dice2, self.missile_damage)

        # spells
        if self.spells:
            for spell in self.spells:
                output = output + spell.to_string()

        # affects
        if self.affects and self.affects > 0:
            output = output + "Affects:\n"
            for affect in self.affects:
                output = output + affect.to_string()

        # modifiers
        if self.modifiers and self.modifiers > 0:
            output = output + "Skill/Spell Modifiers: \n"
            for modifier in self.modifiers:
                output = output + modifier.to_string()

        return output

    def is_equal(self, item2):
        if self.name != item2.name:
            return False

        # check modifiers
        if len(self.modifiers) != len(item2.modifiers):
            return False

        for mod in self.modifiers:
            found = False
            for other_mod in item2.modifiers:
                if mod.is_equal(other_mod):
                    found = True
                    break
            if not found:
                return False

        # check affects
        if len(self.affects) != len(item2.affects):
            return False

        for affect in self.affects:
            found = False
            for other_affect in item2.affects:
                if affect.is_equal(other_affect):
                    found = True
                    break
            if not found:
                return False

        return True


def property_has_value(prop):
    return isinstance(prop, basestring) or isinstance(prop, list)


# Add the item to the database. Return False if the add didn't go through because there is already a duplicate.
def create_or_update_item(item, item_summary):
    if item is None or item_summary is None:
        raise TypeError("item or item_summary was None when attempting to insert item into database")

    # check to see if the item is already in the database, if it is, don't insert another one
    items = Item.query(Item.name == item.name).fetch()
    for db_item in items:
        if db_item.is_equal(item):
            return False

    # no db items are the same, so insert the new item
    item.summary_item_key = item_summary.key
    item.put()
    return True


def delete_item(key):
    if key is None:
        return
    key.delete()


def get_item_count():
    q = Item.query()
    return q.count()


def get_item(item_key):
    item = item_key.get()
    return item


def get_all_items(item_summary):
    return Item.query(Item.summary_item_key == item_summary.key).fetch()


def get_key_name(name, affect_strings):
    if affect_strings and len(affect_strings) > 0:
        affect_strings.sort()
        hash_string = name + "|" + "|".join(affect_strings)
    else:
        hash_string = name
    return hashlib.md5(hash_string).hexdigest()
