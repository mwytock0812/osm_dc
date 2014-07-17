#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# Working regex for street street_re = re.compile(r'\b([Ss]t)(\.|\b)')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

mapping = { r'\b([Ss]t)(\.|\b)': "Street",
            r'\b([Rr]d)(\.|\b)': "Road",
            r'\b([Aa]ve)(\.|\b)': "Avenue",
            r'\b([Dd]r)(\.|\b)': "Drive"
            }

def audit_street_type(street_types, street_name):
    """Add street_type to street_types dictionary if not in expected.

    Format:
    {street_type : set(street_name)}
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    """Return ET element if it is a street."""
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """Return a list of street names"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag in ["node", "relation", "way"]:
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    """Return corrected street name from regex in mapping."""
    for key, value in mapping.iteritems():
        if re.search(key, name):
            new_name = re.sub(key, value, name)
            return new_name

def print_audit(osmfile):
    """Pretty print the st_types dictionary.
    Print name suggestions
    """
    st_types = audit(osmfile)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


if __name__ == '__main__':
    OSMFILE = "sampled_dc.osm"
    print_audit(OSMFILE)
