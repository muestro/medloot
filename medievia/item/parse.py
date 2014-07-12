import medievia.item.item
import medievia.item.modifier
import medievia.item.spell
import medievia.item.affect
import medievia.item.focus
import re


# input argument can be a string split into lines, or a file reader, or anything that can be iterated on a line
# by line basis using the for loop
def parse(input_obj):
    items = []
    item = None

    stale_count = 0

    for line in input_obj:
        raw_string = line.decode('utf-8', 'ignore')
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
                item = medievia.item.item.Item()
            else:
                # we're at a new item.  if item had anything in it we're ok scraping it
                item = medievia.item.item.Item()

        if item is not None:
            # check for staleness.  if stale, then process the item (if it's complete) and continue
            if stale_count >= 5:
                if item.is_populated():
                    items.append(item)
                item = None
                stale_count = 0
                continue

            line_not_stale = line_not_stale | \
                _parse_name(line, item) | \
                _parse_item_type(line, item)

            # only continue filling out an item if it has the other expected data
            if medievia.item.item.property_has_value(item.name):
                line_not_stale = line_not_stale | \
                    _parse_equipable_location(line, item) | \
                    _parse_weight(line, item) | \
                    _parse_condition(line, item) | \
                    _parse_days_left(line, item) | \
                    _parse_focus(line, item) | \
                    _parse_available_weight(line, item) | \
                    _parse_spell(line, item) | \
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
            item.keywords = input_string.split("[")[1].strip("]").split()
        return True
    else:
        return False


# Item Type: MAGIC REGEN   Effects: INVISIBLE BLESS NO-DONATE NO-SACRIFICE  NO-DROP
# Item Type: ARMOR   Effects: INVISIBLE
def _parse_item_type(input_string, item):
    matched = False
    # look for the item type
    if "Item Type:" in input_string:
        item.item_type = input_string.split("Item Type:")[1].split("Effects:")[0].strip().split()
        matched = True

    # look for Effects:
    if "Effects:" in input_string:
        item.effects = input_string.split("Effects:")[1].strip().split()
        matched = True
    return matched


# Equipable Location(s): HIP
# Equipable Location(s): TAKE HOLD
# Equipable Location(s): NECK
# Equipable Location(s): TAKE BODY SHIELD
def _parse_equipable_location(input_string, item):
    # look for equipable location
    if "Equipable Location(s):" in input_string and len(input_string.split("Equipable Location(s):")[1].strip()) > 0:
        item.equipable_locations = input_string.split("Equipable Location(s):")[1].replace('TAKE', '')\
            .strip().split(" ")
        return True
    else:
        return False


def _parse_weight(input_string, item):
    matched = False
    if "Weight:" in input_string and not "Available Weight:" in input_string:
        item.weight = int(input_string.split("Weight:")[1].strip().split()[0])
        matched = True

    if "Value:" in input_string:
        item.value = int(input_string.split("Value:")[1].strip().split()[0])
        matched = True

    if "Level Restriction:" in input_string:
        item.level_restriction = int(input_string.split("Level Restriction:")[1].strip())
        matched = True
    return matched


def _parse_condition(input_string, item):
    if "appears to be in" in input_string \
            or "looks as if it will" in input_string \
            or "is visibly worn down" in input_string \
            or "is visibly crumbling" in input_string:
        item.condition = input_string.strip()
        return True
    else:
        return False


def _parse_days_left(input_string, item):
    if "Days Left:" in input_string:
        if "Infinity" in input_string:
            item.days_left = -1
            item.is_expired = True
        else:
            item.days_left = int(input_string.split("Days Left:")[1].strip())
        return True
    else:
        return False


def _parse_available_weight(input_string, item):
    if "Available Weight:" in input_string:
        item.available_weight = int(input_string.split("Available Weight:")[1].strip().split()[0])
        return True
    else:
        return False


def _parse_ac_apply(input_string, item):
    if "AC-apply of" in input_string:
        item.ac_apply = int(input_string.split("AC-apply of")[1].strip().split(" ")[0])
        return True
    else:
        return False


# Attributes: DAGGER  (BACKSTABBER)
# Attributes: ANTI_MAGE ANTI_CLERIC ANTI_THIEF
# Attributes: ANTI_MAGE ANTI_CLERIC DAGGER  (BACKSTABBER)
# Attributes: None
def _parse_attributes(input_string, item):
    if "Attributes:" in input_string and "None" not in input_string:
        item.attributes = [x.strip("()") for x in input_string.split("Attributes:")[1].strip().split(" ")]
        return True
    else:
        return False


def _parse_damage_dice(input_string, item):
    if "Damage Dice of" in input_string:
        item.damage_dice1 = int(input_string.split("Damage Dice of")[1].strip().split("d")[0])
        item.damage_dice2 = int(input_string.split("Damage Dice of")[1].strip().split("d")[1])
        return True
    else:
        return False


# Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
# Level 30 spell of Resurrect.  Holds 7 charges and has 5 charges left.
# If eaten, this will produce the effects of the Remove Poison spell.
def _parse_spell(input_string, item):
    if "spell of" in input_string and \
            ("level" in input_string or "Level" in input_string) and \
            ("Regenerates" in input_string or "charges left" in input_string):
        spell = medievia.item.spell.Spell()

        spell.name = input_string.split("spell of")[1].strip().split(".")[0]
        spell.level = int(input_string.lower().split("level")[1].split()[0])

        if "Holds" in input_string:
            spell.charges = int(input_string.lower().split("holds")[1].split()[0])
        else:
            spell.charges = int(input_string.lower().split("has")[1].split()[0])

        if "Regenerates" in input_string:
            spell.regenerates = True
        else:
            spell.regenerates = False

        item.spells.append(spell)
        return True
    elif "produce the effects of the" in input_string and " spell" in input_string:
        spell = medievia.item.spell.Spell()
        spell.name = input_string.split("produce the effects of the")[1].strip().split(" spell")[0]
        spell.eaten = True
        item.spells.append(spell)
        return True
    else:
        return False


def _parse_class_restriction(input_string, item):
    if "Class Restrictions:" in input_string:
        item.class_restrictions = input_string.split("Class Restrictions:")[1].strip().split()
        return True
    else:
        return False


#     +4 to DAMROLL
#     +0 to SAVING_SPELL
def _parse_affects(input_string, item):
    if _contains_affect(input_string) and \
       ("+" in input_string or "-" in input_string):
        affect = medievia.item.affect.Affect()
        affect.name = input_string.strip().split("to ")[1]
        affect.value = int(input_string.strip().split(" to")[0])
        item.affects.append(affect)
        return True
    else:
        return False


#     +5% to parry (success)
def _parse_modifiers(input_string, item):
    if _contains_modifier(input_string) and \
       ("+" in input_string or "-" in input_string):
        modifier = medievia.item.modifier.Modifier()
        modifier.name = input_string.strip().split("to ")[1].split("(")[0].strip()
        modifier.value = int(input_string.strip().split("%")[0])
        modifier.descriptor = input_string.strip().split("(")[1].strip(")")
        item.modifiers.append(modifier)
        return True
    else:
        return False


def _parse_focus(input_string, item):
    if "Focus for:" in input_string:
        focus = medievia.item.focus.Focus()
        focus.name = input_string.split()[2].strip()
        item.focus.append(focus)
        return True

    elif "Strength: " in input_string:
        if len(item.focus) > 0:
            if item.focus[-1].strength is None or item.focus[-1].strength == "":
                item.focus[-1].strength = input_string.split()[1].strip()
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
       "to STAMINA" in input_string or \
       "to SAVING_SPELL" in input_string or \
       "to MANA" in input_string or \
       "to SAVING_ROD" in input_string or \
       "to ARMOR" in input_string or \
       "to SAVING_PETRI" in input_string or \
       "to BLUNT_VULNERABILITY" in input_string or \
       "to SHARP_VULNERABILITY" in input_string or \
       "to HOLY_VULNERABILITY" in input_string or \
       "to AGE" in input_string or \
       "to MOVE" in input_string or \
       "to SAVING_BREATH" in input_string:
        return True


def _contains_modifier(input_string):
    if "to disarm (success)" in input_string or \
       "to bash (success)" in input_string or \
       "to rage (efficiency)" in input_string or \
       "to parry (success)" in input_string or \
       "to dodge (success)" in input_string or \
       "to disarm (success)" in input_string or \
       "to defend (proficiency)" in input_string or \
       "to Fireball (proficiency)" in input_string or \
       "to Fireball (manacost)" in input_string or \
       "to Frost Shards (proficiency)" in input_string or \
       "to Dispel Magic (proficiency)" in input_string or \
       "to X-Heal (proficiency)" in input_string or \
       "to Heal (proficiency)" in input_string or \
       "to Harm (proficiency)" in input_string or \
       "to Harm (manacost)" in input_string or \
       "to Hammer of Faith (proficiency)" in input_string or \
       "to Demonfire (proficiency)" in input_string or \
       "to Malediction (success)" in input_string or \
       "to Flamestrike (proficiency success)" in input_string or \
       "to Dispel Magic (manacost)" in input_string:
        return True
