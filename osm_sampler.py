try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
import codecs

def sample_xml(infile, header_len = None, fetch_num = 15):
    """Writes a smaller xml file sampling only fetch_num """

    print "Copying first %i lines of infile as header" % header_len
    # Use codecs for utf-8 to avoid write errors
    outfile = codecs.open("sampled_" + infile, "w", "utf-8")
    if type(header_len) == type(1):
        i = 0
        reader = codecs.open(infile, "r", "utf-8")
        while i < header_len:
            line = reader.readline()
            outfile.write(line)
            i += 1
    
    print "Finding first %i elements of interest" % fetch_num
    element_list = ["node", "way", "relation"]
    for element in element_list:
        i = 0
        counter = 0
        for _, elem in ET.iterparse(infile):
            counter += 1
            if elem.tag == element:
                pretty_elem = prettify(elem)
                outfile.write(pretty_elem)
                i += 1
            if i >= fetch_num:
                print "Parsed %i elements for \"%s\" tag" % (counter, element)
                break
    
    # Write appropriate tail
    print "Writing closing xml tag"
    outfile.write(u'</osm>')
    outfile.close()

    print "Finished parsing infile"      
            
def prettify(elem):
    """Return a pretty-printed XML string for the Element"""
    import xml.dom.minidom as minidom

    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    reparsed = reparsed.toprettyxml(indent = "\t")
    # Removes <?xml> tag from .toprettyxml
    stripped_reparsed = reparsed.split('\n', 1)[1]
    return stripped_reparsed
