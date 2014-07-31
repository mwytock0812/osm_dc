#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def format_valid(key):
    """Return False if problem characters in address key."""
    if problemchars.match(key) == None:
        return True
    else:
        return False

def shape_element(element):
    """Return a JSON-like dictionary of each top-level XML tag,
    element.
    """
    node = {}
    if element.tag == "node" or element.tag == "way":
        # Because 'type' already exists in data use 'elment_type'.
        node["element_type"] = element.tag
        node["created"] = {}

        # Store 'created', 'pos', and all other top-level attributes.
        for attr in element.attrib:
            if attr in CREATED:
                node["created"].update({attr : element.get(attr)})
            elif attr == 'lat' or attr == 'lon':
                lat = float(element.get('lat'))
                lon = float(element.get('lon'))
                node["pos"] = [lat, lon]
            else:
                node[attr] = element.get(attr)
        
        # Store 'address' key and all other 2nd-level attributes.
        tags = element.findall("tag")
        if len(tags) > 0:
            node["address"] = {}
            for tag in tags:
                k = tag.attrib['k']
                v = tag.attrib['v']
                if format_valid(k):
                    # Store tags formatted "addr:"
                    if k[:4] == "addr" and k.find(":", 5) == -1:
                        node["address"].update({k[5:] : v})
                    # Store TIGER-formatted tags using "name:"
                    elif k == "name" and element.tag == "way":
                        node["address"].update({"street" : v})
                    # Ignore entries with 'tiger' and 'source:HFCS'.
                    elif re.search(r'(tiger)[:_]', k) or re.search(r'(source:HFCS)', k):
                        pass
                    else:
                        node[k] = v
            if len(node["address"]) == 0:
                del node["address"]

        # Build node_ref document.
        if element.find("nd") != None:
            node_ref_list = []
            for tag in element.findall("nd"):
                ref = tag.attrib['ref']
                node_ref_list.append(ref)
            node["node_refs"] = node_ref_list
        return node
    else:
        return None

def clean_streets(element):
    """Return an element with cleaned street names given a JSON-
    like dictionary."""
    mapping = { r'\b([Ss][Tt])(\.|\b)': "Street",
            r'\b[Ss][Tt][Rr][Ee][Ee][Tt]\b' : "Street",
            r'\b([Rr][Dd])(\.|\b)': "Road",
            r'\b([Aa][Vv][Ee])(\.|\b)': "Avenue",
            r'\b([Dd][Rr])(\.|\b)': "Drive",
            r'\b([Pp][Ll])(\.|\b)' : "Place",
            r'\b[Ss]\.?[Ww](\.?|\b)' : "SW",
            r'\b[Ss][Oo][Uu][Tt][Hh][Ww][Ee][Ss][Tt]\b' : "SW",
            r'\b[Nn]\.?[Ww](\.?|\b)' : "NW",
            r'\b[Nn][Oo][Rr][Tt][Hh][Ww][Ee][Ss][Tt]\b' : "NW",
            r'\b[Ss]\.?[Ee](\.?|\b)' : "SE",
            r'\b[Ss][Oo][Uu][Tt][Hh][Ee][Aa][Ss][Tt]\b' : "SE",
            r'\b[Ss]\.?[Ww](\.?|\b)' : "NE",
            r'\b[Nn][Oo][Rr][Tt][Hh][Ee][Aa][Ss][Tt]\b' : "NE"}
    try: # Try...except to avoid KeyError
        street = element["address"]["street"]
        for key, value in mapping.iteritems():
            street = re.sub(key, value, street)
        element["address"]["street"] = street
        return element
    except:
        return element

def process_map(file_in, pretty = False):
    """Return a shaped and cleaned JSON file given OSM XML."""
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element) # Shape element
            if el:
                el = clean_streets(el) # Clean element
                pprint.pprint(el)
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == "__main__":
    process_map("dc.osm")
