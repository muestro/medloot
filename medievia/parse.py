import medievia.item
import re


# input argument can be a string split into lines, or a file reader, or anything that can be iterated on a line
# by line basis using the for loop
def parse(input_obj):
    items = []
    item = None

    stale_count = 0

    for line in input_obj:
        raw_string = line
        line_not_stale = False

        if line == "":
            #print "Skipping line", index, ": ", line
            continue

        line = line.strip("#")
        line = line.strip()

        # normalize the spaces
        line = re.sub(' +', ' ', line)

        if _is_beginning_of_item(line):
            if item is not None and item.is_populated():
                # we're at a new item, and finished with the old item
                items.append(item)
                item = medievia.item.Item()
            else:
                # we're at a new item.  if item had anything in it we're ok scraping it
                item = medievia.item.Item()

        if item is not None:
            # check for stale-ness.  if stale, then process the item (if it's complete) and continue
            if stale_count >= 5:
                if item.is_populated():
                    items.append(item)
                item = None
                stale_count = 0
                continue

            line_not_stale = line_not_stale | \
                _parse_name(line, item) | \
                _parse_item_type(line, item)

            # only continue filling out an item if it is has the other expected data
            if medievia.item.property_has_value(item.name):
                line_not_stale = line_not_stale | \
                    _parse_equipable_location(line, item) | \
                    _parse_weight(line, item) | \
                    _parse_condition(line, item) | \
                    _parse_days_left(line, item) | \
                    _parse_charges(line, item) | \
                    _parse_attributes(line, item) | \
                    _parse_ac_apply(line, item) | \
                    _parse_damage_dice(line, item) | \
                    _parse_class_restriction(line, item) | \
                    _parse_affects(line, item) | \
                    _parse_modifiers(line, item)

            if not line_not_stale:
                stale_count += 1
            else:
                stale_count = 0

            item.source_string += raw_string

    if item is not None and item.is_populated():
        items.append(item)

    return items


def _is_beginning_of_item(input_string):
    return _parse_name(input_string, None)


def _parse_name(input_string, item):
    # look for the object title
    if "Object:" in input_string:
        if item:
            item.name = input_string.split("Object:")[1].strip().split("[")[0].strip()

            # look for the object keywords
            item.keywords = medievia.item.listify(input_string.split("[")[1].strip("]").split())
        return True
    else:
        return False


# single value
def _parse_item_type(input_string, item):
    matched = False
    # look for the item type
    if "Item Type:" in input_string:
        item.item_type = input_string.split("Item Type:")[1].strip().split()[0]
        matched = True

    # look for Effects:
    if "Effects:" in input_string:
        item.effects = medievia.item.listify(input_string.split("Effects:")[1].strip().split())
        matched = True
    return matched


def _parse_equipable_location(input_string, item):
    # look for equipable location
    if "Equipable Location(s):" in input_string:
        item.equipable_locations = input_string.split("Equipable Location(s):")[1].strip().split(" ")
        return True
    else:
        return False


def _parse_weight(input_string, item):
    matched = False
    if "Weight:" in input_string and not "Available Weight:" in input_string:
        item.weight = input_string.split("Weight:")[1].strip().split()[0]
        matched = True

    if "Value:" in input_string:
        item.value = input_string.split("Value:")[1].strip().split()[0]
        matched = True

    if "Level Restriction:" in input_string:
        item.level_restriction = input_string.split("Level Restriction:")[1].strip()
        matched = True
    return matched


def _parse_condition(input_string, item):
    if "appears to be in" in input_string or "looks as if it will" in input_string:
        item.condition = input_string.strip()
        return True
    else:
        return False


def _parse_days_left(input_string, item):
    if "Days Left:" in input_string:
        item.days_left = input_string.split("Days Left:")[1].strip()
        return True
    else:
        return False


def _parse_ac_apply(input_string, item):
    if "AC-apply of" in input_string:
        item.ac_apply = input_string.split("AC-apply of")[1].strip().split(" ")[0]
        return True
    else:
        return False


def _parse_attributes(input_string, item):
    if "Attributes:" in input_string:
        item.attributes = [x.strip("()") for x in input_string.split("Attributes:")[1].strip().split(" ")]
        return True
    else:
        return False


def _parse_damage_dice(input_string, item):
    if "Damage Dice of" in input_string:
        item.damage_dice1 = input_string.split("Damage Dice of")[1].strip().split("d")[0]
        item.damage_dice2 = input_string.split("Damage Dice of")[1].strip().split("d")[1]
        return True
    else:
        return False


def _parse_charges(input_string, item):
    if input_string.startswith("Has") and "charges left" in input_string:
        item.charges = input_string.split(" ")[1].strip()
        return True
    else:
        return False


def _parse_class_restriction(input_string, item):
    if "Class Restrictions:" in input_string:
        item.class_restrictions = medievia.item.listify(input_string.split("Class Restrictions:")[1].strip().split())
        return True
    else:
        return False


def _parse_affects(input_string, item):
    if _contains_affect(input_string) and \
       ("+" in input_string or "-" in input_string):
        item.affects.append(input_string)
        return True
    else:
        return False


def _parse_modifiers(input_string, item):
    if _contains_modifier(input_string) and \
       ("+" in input_string or "-" in input_string):
        item.modifiers.append(input_string)
        return True
    else:
        return False


def _contains_affect(input_string):
    if "to HITROLL" in input_string or \
       "to DAMROLL" in input_string or \
       "to HIT_POINTS" in input_string or \
       "to INFLUENCE_MELEE" in input_string or \
       "to INFLUENCE_SPELLS" in input_string or \
       "to STR" in input_string or \
       "to INT" in input_string or \
       "to WIS" in input_string or \
       "to DEX" in input_string or \
       "to CON" in input_string or \
       "to SAVING_SPELL" in input_string or \
       "to MANA" in input_string or \
       "to SAVING_ROD" in input_string or \
       "to ARMOR" in input_string or \
       "to SAVING_PETRI" in input_string or \
       "to BLUNT_VULNERABILITY" in input_string or \
       "to SHARP_VULNERABILITY" in input_string or \
       "to SAVING_BREATH" in input_string:
        return True


def _contains_modifier(input_string):
    if "to disarm (success)" in input_string or \
       "to rage (efficiency)" in input_string or \
       "to parry (success)" in input_string or \
       "to parry (success)" in input_string or \
       "to disarm (success)" in input_string or \
       "to Fireball (proficiency)" in input_string or \
       "to Fireball (manacost)" in input_string or \
       "to Frost Shards (proficiency)" in input_string or \
       "to Dispel Magic (proficiency)" in input_string or \
       "to X-Heal (proficiency)" in input_string or \
       "to Harm (proficiency)" in input_string or \
       "to Hammer of Faith (proficiency)" in input_string or \
       "to Demonfire (proficiency)" in input_string or \
       "to Dispel Magic (manacost)" in input_string:
        return True