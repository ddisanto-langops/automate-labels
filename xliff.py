import xml.etree.ElementTree as ET

class XLIFF:
    """
    Class XLIFF represents a downloaded XLIFF file.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.contents = []

    def load_contents(self):
        """        
        Returns XLIFF contents as list of dicts: [{id:12345, source "text, etc."}]
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing XLIFF file: {e}")
            return []

        namespace = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
        extracted_data = []
        for trans_unit in root.findall('.//xliff:trans-unit', namespace):
            unit_id = trans_unit.get('id')  # Get the 'id' attribute of the trans-unit
            source_element = trans_unit.find('xliff:source', namespace)
            if source_element is not None:
                source_text = ''.join(source_element.itertext())
                extracted_data.append({'id': unit_id, 'source': source_text.strip()})

        self.contents = extracted_data
        return extracted_data