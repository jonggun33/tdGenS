import json
from xml.dom import minidom
import xml.etree.ElementTree as ET

def json_to_xml(json_data, root_name="root"):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    root = ET.Element(root_name)
    _build_xml(root, json_data)
    return _prettify_xml(root)

def _build_xml(parent, data):
    """Recursively build XML tree from JSON data."""
    if isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            _build_xml(child, value)
    elif isinstance(data, list)  :
        for item in data:
            if parent.tag== "DataS":
                child = ET.SubElement(parent, "Data")
            else:
                child = ET.SubElement(parent, "Component")
            _build_xml(child, item)
    else:
        parent.text = str(data)

def _prettify_xml(elem):
    """Return a pretty-printed XML string."""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml(indent="  ")
    # Remove lines for <Data> and </Data>
    lines = pretty.splitlines()
    lines = lines[1:]  # Skip the XML declaration
    lines = [line for line in lines if line.strip() not in ['<DataS>', '</DataS>']]
    return '\n'.join(lines)