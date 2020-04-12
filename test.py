import os
import xml.etree.ElementTree as ET
xml_tree = ET.parse(os.path.join(os.getcwd(), 'conf', 'url-mapping.xml'))
uriList = xml_tree.getroot().findall('uri')

func = lambda uri:map(uri.get, [k for k in uri.keys() if k=='name' or k == 'func'])
{data[0]:data[1] for data in map(func, uriList) if data != []}
