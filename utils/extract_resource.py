import json
import matplotlib.image as Image
# from geefusion_project_server.projects.models import Resource
from datetime import datetime
from xmlconverter import XMLConverter
from search import exists_with_version, get_version_xml

with open("./config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"


def extract_resource(path, version, resolution):
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        print(reason)
        return None
    
    # Get resource xml
    xml_path = get_version_xml(path, version)

    resource_name = path.split("=")[0].split("/")[-1].split(".")[0]
    extent, thumbnail, creation_date = get_resource_data(xml_path)
    print([resource_name, extent, creation_date, resolution])

    # return Resource()


def get_resource_data(xml_path):
    json = XMLConverter.convert(xml_path)
    metadata = json["meta"]["item"]

    extent = metadata[1]
    thumbnail = Image.imread(ASSETS_PATH + metadata[-2])
    creation_date = datetime.strptime(metadata[-1], '%Y-%m-%dT%H:%M:%SZ')

    return [ extent, thumbnail, creation_date]