import os
import xml.etree.ElementTree as ET
xml_tree = ET.parse(os.path.join(os.getcwd(), 'conf', 'url-mapping.xml'))
uriAttr = xml_tree.getroot().findall('uri')
rootPack = xml_tree.getroot().find('root-package')
print {uri.attrib['target']:{x.attrib['type'].upper():x.attrib['func'] for x in uri} for uri in uriAttr}
print rootPack.attrib['value']
