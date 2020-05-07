from xml.etree.ElementTree import fromstring
from json import dump, dumps
import xmljson
import xmltodict

class XMLConverter:

    @staticmethod
    def convert(xml_path, save_attributes=False):

        converter = xmljson.badgerfish if save_attributes else xmljson.parker

        with open(xml_path, 'r') as file:
            text = file.read()
            data = converter.data(fromstring(text))
            # data = converter.data(fromstring(text), preserve_root=True)
            return data

    @staticmethod
    def convert_and_save(xml_path, file_name, save_attributes=False):

        with open(file_name + ".json", 'w') as json_file:
            dump(XMLConverter.convert(xml_path, save_attributes), json_file, ensure_ascii=False, indent=4)