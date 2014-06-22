from google.appengine.ext import ndb

import medievia.item.modifier
import medievia.item.spell
import medievia.item.item_base
import medievia.item.affect


class ItemSummary(medievia.item.item_base.ItemBase):

    # +X% to parry/rage/disarm/X-Heal/Hammer of Faith/Demonfire/Harm (success/efficiency/proficiency)
    base_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)
    min_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)
    max_modifiers = ndb.StructuredProperty(medievia.item.modifier.Modifier, repeated=True)

    # affects
    base_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)
    min_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)
    max_affects = ndb.StructuredProperty(medievia.item.affect.Affect, repeated=True)


def _create_item_summary(item):
    item_summary = ItemSummary()
    medievia.item.item_base.copy_attributes(item, item_summary)

    return item_summary


def create_or_update_item_summary(item):
    # check the database to see if it already exists, if so retrieve it
    item_summary = _get_item_summary_from_db(item.name)
    if item_summary is None:
        item_summary = _create_item_summary(item)

    # for each property set its min max and base
    for modifier in item.modifiers:
        # get the existing min/max/base values from the summary item.  if they're not there then we'll create new ones
        min_prop = _get_same_property_from_list(item_summary.min_modifiers, modifier)
        max_prop = _get_same_property_from_list(item_summary.max_modifiers, modifier)
        base_prop = _get_same_property_from_list(item_summary.base_modifiers, modifier)

        if min_prop is None:
            # create a new property and add it
            min_prop = modifier.copy()
            item_summary.min_modifiers.append(min_prop)

        if max_prop is None:
            # create a new property and add it
            max_prop = modifier.copy()
            item_summary.max_modifiers.append(max_prop)

        if base_prop is None and item.is_expired:
            # create a new property and add it
            base_prop = modifier.copy()
            item_summary.base_modifiers.append(base_prop)

        # set the new min, max, and base values
        min_prop.value = min(modifier.value, min_prop.value)
        max_prop.value = max(modifier.value, max_prop.value)

        if item.is_expired:
            base_prop.value = max(modifier.value, base_prop.value)

    for affect in item.affects:
        # get the existing min/max/base values from the summary item.  if they're not there then we'll create new ones
        min_prop = _get_same_property_from_list(item_summary.min_affects, affect)
        max_prop = _get_same_property_from_list(item_summary.max_affects, affect)
        base_prop = _get_same_property_from_list(item_summary.base_affects, affect)

        if min_prop is None:
            # create a new property and add it
            min_prop = affect.copy()
            item_summary.min_affects.append(min_prop)

        if max_prop is None:
            # create a new property and add it
            max_prop = affect.copy()
            item_summary.max_affects.append(max_prop)

        if base_prop is None and item.is_expired:
            # create a new property and add it
            base_prop = affect.copy()
            item_summary.base_affects.append(base_prop)

        # set the new min, max, and base values
        min_prop.value = medievia.item.affect.get_worse_affect(affect, min_prop).value
        max_prop.value = medievia.item.affect.get_better_affect(affect, max_prop).value

        if item.is_expired:
            base_prop.value = medievia.item.affect.get_better_affect(affect, base_prop).value

    item_summary.put()
    return item_summary


# attempts to find the existing property from the summary item.
def _get_same_property_from_list(property_list, reference_property):
    for prop in property_list:
        if prop.is_same_type(reference_property):
            return prop
    return None


def _get_item_summary_from_db(name):
    result = ItemSummary.query(ItemSummary.name == name).fetch(1)
    if result is not None and len(result) > 0:
        return result[0]
    return None