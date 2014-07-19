import medievia.item.item
import medievia.item.modifier
import medievia.item.spell
import medievia.item.affect
import medievia.item.focus


def is_single_line_item(input_string):
    return "Lev(" in input_string and \
           "Loc(" in input_string and \
           "Cond(" in input_string


def parse(input_string):
    name = input_string.split("- Lev")[0].split(">")[1].strip()
    return None