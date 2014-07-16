#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    """Return a dictionary counting number of top-level tags.

    Dictionary Format:
    {tag_name : count}
    """
    # Initialize ouput dict. Build and root tree.
    tags = {}
    tree = ET.parse(filename)
    root = tree.getroot()

    # Count top-level tag appearances by line in root.
    for line in root:
        if line.tag in tags:
            count = tags[line.tag]
            tags[line.tag] = count + 1
        else:
            tags[line.tag] = 1
    return tags

def print_tags(osmfile):
    """Pretty prints dictionary of tag counts."""
    tags = count_tags(osmfile)
    pprint.pprint(tags)

if __name__ == "__main__":
    OSMFILE = "sampled_dc.osm"
    print_tags(OSMFILE)
