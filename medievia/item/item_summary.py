from google.appengine.ext import ndb

import medievia.item.modifier
import medievia.item.spell
import medievia.item.item_base


class ItemSummary(medievia.item.item_base.ItemBase):

    # +X% to parry/rage/disarm/X-Heal/Hammer of Faith/Demonfire/Harm (success/efficiency/proficiency)
    base_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)
    min_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)
    max_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)

    # Regenerates level 26 spell of Bloodbath.  Has 1 maximum charges.
    # Regenerates level 25 spell of Iceshield.  Has 5 maximum charges.
    base_spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)
    min_spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)
    max_spells = ndb.StructuredProperty(medievia.item.spell.Spell, repeated=True)

    # affects
    base_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)
    min_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)
    max_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)


def _create_item_summary(item):
    item_summary = ItemSummary()
    found_property = False
    for prop in dir(item):
        attr = getattr(item, prop)
        if not prop.startswith("_") and isinstance(attr, ndb.Property):
            setattr(item_summary, prop, attr)
            found_property = True

    if found_property:
        return item_summary
    else:
        return None


def create_or_update_item_summary(item):
    # check the database to see if it already exists, if so retrieve it
    if False:
        # found the item in the db
        item_summary = None
    else:
        item_summary = _create_item_summary(item)

    # for each property set its min max and base
    for modifier in item.modifiers:
        _set_min_max_base(modifier, item_summary.min_modifiers, item_summary.max_modifiers, item_summary.base_modifiers,
                          item.is_expired)

    for affect in item.affects:
        _set_min_max_base(affect, item_summary.min_affects, item_summary.max_affects, item_summary.base_affects,
                          item.is_expired)

    for spell in item.spells:
        _set_min_max_base(spell, item_summary.min_spells, item_summary.max_spells, item_summary.base_spells,
                          item.is_expired)

    item_summary.put()
    return item_summary


def _set_min_max_base(prop, s_min_properties, s_max_properties, s_base_properties, is_expired):
    # check if the property exists on the summary
    try:
        s_min = next(x for x in s_min_properties if x.name == prop.name)
        s_max = next(x for x in s_max_properties if x.name == prop.name)
    except StopIteration:
        # prop isn't in item summary
        pass

    # check base separately
    try:
        s_base = next(x for x in s_base_properties if x.name == prop.name)
    except StopIteration:
        # prop isn't in item summary
        pass

    if s_min is None or s_min.value > prop.value:
        s_min = prop.copy()

    if s_max is None or s_max.value < prop.value:
        s_max = prop.copy()

    if is_expired and (s_base is None or s_base.value < prop.value):
        s_base = prop.copy()