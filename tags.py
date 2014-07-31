#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    """Update a dictionary counting the number of tag attributes
    in an ET element that contain characters of interest.
    """
    if element.tag == "tag":
        k = element.attrib['k']
        if len(lower_colon.findall(k)) > 0:
            keys['lower_colon'] += 1
        elif len(lower.findall(k)) > 0:
            keys['lower'] += 1
        elif problemchars.match(k):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys

def process_map(filename):
    """Return the keys dictionary after parsing the whole XML file."""
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

if __name__ == "__main__":
    keys = process_map('dc.osm')
    pprint.pprint(keys)
