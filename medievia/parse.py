import medievia.item
import re


# TODO: parse only supports a single object atm.
def parse(input_string):
    lines = [s.strip() for s in input_string.splitlines()]

    item = medievia.item.Item()

    for index, line in enumerate(lines):
        if line == "":
            #print "Skipping line", index, ": ", line
            continue

        # normalize the spaces
        line = re.sub(' +', ' ', line)

        _parse_name(line, item)
        _parse_item_type(line, item)
        _parse_equipable_location(line, item)
        _parse_weight(line, item)
        _parse_condition(line, item)
        _parse_days_left(line, item)
        _parse_charges(line, item)
        _parse_attributes(line, item)
        _parse_ac_apply(line, item)
        _parse_damage_dice(line, item)
        _parse_class_restriction(line, item)
        _parse_affects(line, item)

    return item


def _parse_name(input_string, item):
    # look for the object title
    if "Object:" in input_string:
        item.name = input_string.split("Object:")[1].strip().split("[")[0].strip()

        # look for the object keywords
        item.keywords = medievia.item.listify(input_string.split("[")[1].strip("]").split())


# single value
def _parse_item_type(input_string, item):
    # look for the item type
    if "Item Type:" in input_string:
        item.item_type = input_string.split("Item Type:")[1].strip().split()[0]

    # look for Effects:
    if "Effects:" in input_string:
        item.effects = medievia.item.listify(input_string.split("Effects:")[1].strip().split())


def _parse_equipable_location(input_string, item):
    # look for equipable location
    if "Equipable Location(s):" in input_string:
        item.equipable_locations = input_string.split("Equipable Location(s):")[1].strip().split(" ")


def _parse_weight(input_string, item):
    if "Weight:" in input_string:
        item.weight = input_string.split("Weight:")[1].strip().split()[0]

    if "Value:" in input_string:
        item.value = input_string.split("Value:")[1].strip().split()[0]

    if "Level Restriction:" in input_string:
        item.level_restriction = input_string.split("Level Restriction:")[1].strip()


def _parse_condition(input_string, item):
    if "appears to be in" in input_string or "looks as if it will" in input_string:
        item.condition = input_string.strip()


def _parse_days_left(input_string, item):
    if "Days Left:" in input_string:
        item.days_left = input_string.split("Days Left:")[1].strip()


def _parse_ac_apply(input_string, item):
    if "AC-apply of" in input_string:
        item.ac_apply = input_string.split("AC-apply of")[1].strip().split(" ")[0]


def _parse_attributes(input_string, item):
    if "Attributes:" in input_string:
        item.attributes = [x.strip("()") for x in input_string.split("Attributes:")[1].strip().split(" ")]


def _parse_damage_dice(input_string, item):
    if "Damage Dice of" in input_string:
        item.damage_dice1 = input_string.split("Damage Dice of")[1].strip().split("d")[0]
        item.damage_dice2 = input_string.split("Damage Dice of")[1].strip().split("d")[1]


def _parse_charges(input_string, item):
    if input_string.startswith("Has") and "charges left" in input_string:
        item.charges = input_string.split(" ")[1].strip()


def _parse_class_restriction(input_string, item):
    if "Class Restrictions:" in input_string:
        item.class_restrictions = medievia.item.listify(input_string.split("Class Restrictions:")[1].strip().split())


def _parse_affects(input_string, item):
    if ("+" in input_string or "-" in input_string) and " to " in input_string:
        item.affects.append(input_string)
