#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re

def get_user(element):
    """Return user ID for an element."""
    uid = element.attrib['uid']
    return uid


def unique_users(filename):
    """Return a set of unique user IDs (uids)
    **Formerly process_map(filename)**
    """
    users = set()
    for event, element in ET.iterparse(filename):
        if element.tag in ['node', 'way', 'relation']:
            users.add(get_user(element))
    return users

if __name__ == "__main__":
    users = unique_users("sampled_dc.osm")
    pprint.pprint(users)
    print "Unique users: %i" % len(users)
