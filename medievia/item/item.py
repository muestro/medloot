from google.appengine.ext import db
import hashlib


# model object
class Item(db.Model):
    name = db.StringProperty()
    keywords = db.StringListProperty()
    item_type = db.StringProperty()
    effects = db.StringListProperty()
    equipable_locations = db.StringListProperty()
    weight = db.StringProperty()
    value = db.StringProperty()
    level_restriction = db.StringProperty()
    condition = db.StringProperty()
    days_left = db.StringProperty()
    class_restrictions = db.StringListProperty()
    affects = db.StringListProperty()
    modifiers = db.StringListProperty()

    charges = db.StringProperty()
    attributes = db.StringListProperty()
    damage_dice1 = db.StringProperty()
    damage_dice2 = db.StringProperty()
    ac_apply = db.StringProperty()

    is_expired = db.BooleanProperty()

    source_string = ''

    # todo: change the affects to be their own separate object.
    # Make the property in this class be a ListProperty(db.Key)
    # Make sure to consider efficiency,
    # re: http://stackoverflow.com/questions/4719700/list-of-references-in-google-app-engine-for-python
    # re: http://blog.notdot.net/2010/01/ReferenceProperty-prefetching-in-App-Engine
    # affects_ref = db.ListProperty(db.Key)

    def get_effect_value(self, effect_name):
        return effect_name in self.effects

    def get_affect_value(self, affect_name):
        affect_value = 0
        has_affect = False
        for affect in self.affects:
            if affect_name in affect:
                has_affect = True
                affect_value += int(affect.split(" ")[0])

        if has_affect:
            return affect_value
        else:
            return ""

    def is_populated(self):
        return property_has_value(self.name) and property_has_value(self.keywords) \
            and property_has_value(self.item_type)

    def to_dict(self):
        return db.to_dict(self)

    def to_string(self):
        # object, name, keywords
        output = "Object: {0} [{1}]\n".format(self.name, ", ".join(self.keywords))

        # item type, effects
        output = output + "Item Type: {0} \tEffects: {1}\n".format(self.item_type, " ".join(self.effects))

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

        # charges
        if self.charges:
            output = output + "Has {0} charges left.\n".format(self.charges)

        # class restrictions
        if self.class_restrictions:
            output = output + "Class Restrictions: {0}\n".format(" ".join(self.class_restrictions))

        # affects
        if self.affects:
            output = output + "Affects: \n\t{0}\n".format("\n\t".join(self.affects))

        # modifiers
        if self.modifiers:
            output = output + "Skill/Spell Modifiers: \n\t{0}\n".format("\n\t".join(self.modifiers))

        return output


def property_has_value(prop):
    return isinstance(prop, basestring) or isinstance(prop, list)


# db CRUD ops
def create_or_update_item(item):
    if item is None:
        return
    item.put()

    # update the corresponding item_info
    _update_item_info(item)


def delete_item(key):
    if key is None:
        return

    item = db.get(db.Key(key))
    item.delete()


def get_items(name=None):
    if name is not None:
        items = db.GqlQuery('SELECT * FROM Item WHERE name = :1', name).run()
    else:
        items = db.GqlQuery('SELECT * FROM Item').run()
    return items


def get_item_count():
    q = db.Query(ItemSummary)
    return q.count()


def get_item(item_key):
    try:
        item = db.get(db.Key(item_key))
    except db.BadKeyError:
        return

    return item


def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj


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
