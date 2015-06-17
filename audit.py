#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons",
            "SW", "NW", "SE", "NE"]


mapping = { r'\b([Ss][Tt])(\.|\b)': "Street",
            r'\b[Ss][Tt][Rr][Ee][Ee][Tt]\b': "Street",
            r'\b([Rr][Dd])(\.|\b)': "Road",
            r'\b([Aa][Vv][Ee])(\.|\b)': "Avenue",
            r'\b([Dd][Rr])(\.|\b)': "Drive",
            r'\b([Pp][Ll])(\.|\b)': "Place",
            r'\b[Ss]\.?[Ww](\.?|\b)': "SW",
            r'\b[Ss][Oo][Uu][Tt][Hh][Ww][Ee][Ss][Tt]\b': "SW",
            r'\b[Nn]\.?[Ww](\.?|\b)': "NW",
            r'\b[Nn][Oo][Rr][Tt][Hh][Ww][Ee][Ss][Tt]\b': "NW",
            r'\b[Ss]\.?[Ee](\.?|\b)': "SE",
            r'\b[Ss][Oo][Uu][Tt][Hh][Ee][Aa][Ss][Tt]\b': "SE",
            r'\b[Ss]\.?[Ww](\.?|\b)': "NE",
            r'\b[Nn][Oo][Rr][Tt][Hh][Ee][Aa][Ss][Tt]\b': "NE"
            }


def audit_street_type(street_types, street_name):
    """Add street_type to street_types dictionary if not in expected.
    Format: {street_type : set(street_name)}
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
    """Return a list of street names not in expected."""
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
    """Pretty print the st_types dictionary and suggested changes."""
    st_types = audit(osmfile)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

if __name__ == '__main__':
    OSMFILE = "dc.osm"
    print_audit(OSMFILE)
