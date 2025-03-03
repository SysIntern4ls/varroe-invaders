import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

class SaveManager:
    def __init__(self, elementName: str):
        self.saveFile = elementName + ".xml"
        self.elementName = elementName
        self.saveData = {}

    def load(self, subElementName: str):
        if os.path.exists(self.saveFile):
            try:
                tree = ET.parse(self.saveFile)
                root = tree.getroot()
                
                # Check if subElementName exists before attempting to load
                elements = root.findall(subElementName)
                if elements:
                    self.saveData = {save.get("name"): save.text for save in elements}
                else:
                    print(f"Warning: No elements found for '{subElementName}'. Resetting.")
                    self.saveData = {}

            except ET.ParseError:
                print("Error: Could not parse XML file. Resetting.")
                self.saveData = {}
        else:
            print(f"Warning: File '{self.saveFile}' not found. Creating a new one on save.")
            self.saveData = {}

    def save(self, subElementName: str):
        # Saves data with pretty-print formatting
        root = ET.Element(self.elementName)
        for key, value in self.saveData.items():
            setting = ET.SubElement(root, subElementName, name=key)
            setting.text = str(value)  # Convert value to string

        # Convert to string and pretty-print using minidom
        xml_str = ET.tostring(root, encoding="utf-8")
        pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")

        # Write the formatted XML to the file
        with open(self.saveFile, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        
