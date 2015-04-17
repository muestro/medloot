import medievia.item.item
import medievia.item.modifier
import medievia.item.spell
import medievia.item.affect
import medievia.item.focus
import re


class_restriction_strings = {
    'AM': 'ANTI_MAGE',
    'AT': 'ANTI_THIEF',
    'AW': 'ANTI_WARRIOR',
    'AC': 'ANTI_CLERIC',
    '2H': 'TWO_HANDED'
}

effect_strings = {
    'AE': 'ANTI-EVIL',
    'AN': 'ANTI-NEUTRAL',
    'AG': 'ANTI-GOOD',
    'noegg': 'NOEGG', #?
    'nounegg': 'NO-UNEGG',
    'norent': 'NO_RENT', #?
    'present': 'PRESENT', #?
    'qprize': 'QPRIZE',
    'holy': 'HOLY',
    'evil': 'EVIL',
    'attack': 'ATTACK',
    'SE': 'SMITE-EVIL',
    'SG': 'SMITE-GOOD',
    'SN': 'SMITE-NEUTRAL',
    'fire': 'FIRE',
    'cold': 'COLD',
    'electric': 'ELECTRIC',
    'glow': 'GLOW',
    'hum': 'HUM',
    'magic': 'MAGIC',
    'bless': 'BLESS',
    'donation': 'DONATION',
    'fragile': 'FRAGILE',
    'clan': 'CLAN'
}

attribute_strings = {
    'DAG': 'DAGGER',
    'BSER': 'BACKSTABBER'
    # 2 handed?
}

affect_strings = {'hr': 'HITROLL',
                  'dr': 'DAMROLL',
                  'hps': 'HIT_POINTS',
                  'mana': 'MANA',
                  'infmel': 'INFLUENCE_MELEE',
                  'infspl': 'INFLUENCE_SPELLS',
                  'infcler': 'INFLUENCE_CLERIC',
                  'str': 'STR',
                  'int': 'INT',
                  'wis': 'WIS',
                  'dex': 'DEX',
                  'con': 'CON',
                  'sta': 'STAMINA',
                  'ss': 'SAVING_SPELL',
                  'srod': 'SAVING_ROD',
                  'sp': 'SAVING_PETRI',
                  'sb': 'SAVING_BREATH',
                  'armor': 'ARMOR',
                  'bluntvuln': 'BLUNT_VULNERABILITY',
                  'sharpvuln': 'SHARP_VULNERABILITY',
                  'holyvuln': 'HOLY_VULNERABILITY',
                  'firevuln': 'FIRE_VULNERABILITY',
                  'age': 'AGE',
                  'mv': 'MOVE'
                  }

equipable_location_strings = {
    'FING': 'FINGER'
}

condition_strings = {
    'pristine': 'The object appears to be in perfect pristine condition.',
    'excellent': 'The object appears to be in excellent condition.',
    'good': 'The object appears to be in good condition.',
    'fair': 'The object appears to be in fair condition.',
    'scratched': 'The object is in fair condition but has some scratches.',
    'worn': 'This object clearly shows major signs of wear and tear.',
    'worn down': 'The object is visibly worn down with major wear.',
    'ending': 'The life of this object is clearly coming to an end soon.',
    'any day': 'The object looks as if it will fall apart any day now.',
    'crumbling': 'The object is visibly crumbling and decaying....',
    'nodet': 'This object has been blessed by the Gods and seems indestructible.'
}


def remove_noise(input_string):
    input_string = input_string.strip()

    # remove the <worn on|as|around> prefixes
    if re.match(r"^<[^>]+>(.*)", input_string):
        input_string = re.match(r"^<[^>]+>(.*)", str).group(1)



    if ", '" in input_string:
        input_string = input_string.split(", '")[1]
    if ")'." in input_string:
        input_string = input_string.split("'.")[0]
    return input_string


def is_single_line_item(input_string):
    return "Lev(" in input_string and \
           "Loc(" in input_string and \
           "Cond(" in input_string


# a massive battleplate - Lev(23) Loc(body) AM AT AW AC-ap(8) AE hps(37) ss(-2) Cond(any day - Egged - fnt grn - 49 Days)
def parse(input_string):
    item = medievia.item.item.Item()

    # remove beginning and end noise
    input_string = remove_noise(input_string)

    # name
    name = input_string.split(" - Lev")[0]
    if ">" in name:
        name = name.split(">")[1].strip()
    item.name = name

    # level
    level = int(input_string.split("Lev(")[1].split(")")[0].strip())
    item.level_restriction = level

    # equipable locations
    equipable_locations = input_string.split("Loc(")[1].split(")")[0].strip().upper().split()
    equipable_locations = [equipable_location_strings[el] if el in equipable_location_strings.keys() else el
                           for el in equipable_locations]
    item.equipable_locations = equipable_locations

    # condition
    condition = input_string.split("Cond(")[1].split(")")[0].strip().split(" - ")[0]
    if condition in condition_strings.keys():
        item.condition = condition_strings[condition]

    # days left
    days_left = input_string.split("Cond(")[1].split(")")[0].strip().split(" - ")
    days_left = days_left[-1].split(" ")[0]
    if days_left == "Infinity":
        days_left = -1
    item.days_left = int(days_left)

    # missile damage
    if " missile by " in input_string:
        item.missile_damage = float(input_string.split("missile by ")[1].split()[0].strip())

    # skl/spl
    # X-Heal (proficiency +8%) Harm (proficiency -48%) Hammer of Faith (proficiency -48%) Demonfire (proficiency -49%)
    if "SKL/SPL:" in input_string:
        skill_spell_input_string = input_string.split("SKL/SPL:")[1].strip().split("Cond(")[0].strip()
        spell_skill_groups = re.findall(r"([^\(]+) \((\w+) ([\+-][\d]+)%\)", skill_spell_input_string)
        for spell_skill_group in spell_skill_groups:
            # [('X-Heal', 'proficiency', '+8'), ('Harm', 'proficiency', '-48'), ('Faith', 'proficiency', '-48'),
            #   ('Demonfire', 'proficiency', '-49')]
            modifier = medievia.item.modifier.Modifier()
            modifier.name = spell_skill_group[0].strip()
            modifier.descriptor = spell_skill_group[1].strip()
            modifier.value = int(spell_skill_group[2].strip())
            item.modifiers.append(modifier)

    # trim the string to just contain affects, modifiers, restrictions
    inner_input_string = input_string\
        .split("Loc(")[1].split(") ", 1)[1].strip()\
        .split("Cond(")[0].strip()\
        .split("SKL/SPL:")[0].strip()

    # AM AT AW AC-ap(8) AE hps(37) ss(-2)
    class_restrictions = set()
    affects = []
    effects = []
    attributes = []
    spells = []
    for property_string in inner_input_string.split():
        # damage dice check
        if re.match(r"(\d+)d(\d+)", property_string):
            damage_dice = re.findall(r"\d+", property_string)
            item.damage_dice1 = int(damage_dice[0])
            item.damage_dice2 = int(damage_dice[1])

        # restriction check
        if property_string in class_restriction_strings.keys():
            class_restrictions.add(class_restriction_strings[property_string])
            continue

        # AC check
        if "AC-ap" in property_string:
            item.ac_apply = int(property_string.split("(")[1].strip(")"))
            continue

        # effect check
        if property_string in effect_strings.keys():
            effects.append(effect_strings[property_string])
            continue

        # attribute check
        if property_string in attribute_strings.keys():
            attributes.append(attribute_strings[property_string])
            continue

        # spells check - Eat(Sanctuary) - 5xResurrect
        if "Eat(" in property_string:
            spell = medievia.item.spell.Spell()
            spell.name = property_string.split("Eat(")[1].strip(")")
            spell.eaten = True
            spells.append(spell)
            continue

        spell_regex_match = re.match(r"(\d+)x(\w+)", property_string)
        if spell_regex_match:
            spell = medievia.item.spell.Spell()
            spell.name = spell_regex_match.group(2)
            spells.append(spell)
            # note we don't get max charges in single line format, only remaining charges which we don't care about

        # affect check
        # affects have name(value) format
        if "(" in property_string and ")" in property_string:
            property_name = property_string.split("(")[0]
            property_value = int(property_string.split("(")[1].strip(")"))

            if property_name in affect_strings.keys():
                affect = medievia.item.affect.Affect()
                affect.name = affect_strings[property_name]
                affect.value = property_value
                affects.append(affect)
                continue

        # modifier check

    item.effects = effects
    item.affects = affects
    item.class_restrictions = class_restrictions
    item.attributes = attributes
    item.spells = spells

    return item