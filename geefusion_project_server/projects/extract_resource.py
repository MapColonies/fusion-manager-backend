import json
import matplotlib.image as Image
from .models import Resource
# from geefusion_project_server.projects.models import Resource
from datetime import datetime
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml
import base64
from django.core.files.base import ContentFile

with open("projects/config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
RESOURCE_PATH = ASSETS_PATH + "Resources/Imagery/"


def get_resource(path, version):
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        print(reason, path)
        return [None, reason]
    
    # Get resource xml
    xml_path = get_version_xml(path, version)

    resource_name = path.split("=")[0].split("/")[-1].split(".")[0]
    extent, thumbnail, creation_date, resolution = get_resource_data(xml_path)

    print(thumbnail)
    # with open(thumbnail, "rb") as image:
    resource = Resource(name=resource_name, version=version, extent=extent, takenAt=creation_date, resolution=resolution)
    resource.thumbnail.save(thumbnail[0], thumbnail[1])
    resource.save()
    return [resource, '']


def get_resource_by_name(name, version):

    path = RESOURCE_PATH + name
    return get_resource(path, version)


def get_resource_data(xml_path):
    json = XMLConverter.convert(xml_path)
    metadata = json["meta"]["item"]

    extent = str(metadata[1])
    # thumbnail = Image.imread(ASSETS_PATH + metadata[-2])
    # thumbnail = ASSETS_PATH + metadata[-2]
    with open(ASSETS_PATH + metadata[-2], 'rb') as file:
        thumbnail = [metadata[-2], ContentFile(base64.b64encode(file.read()))]
    creation_date = datetime.strptime(metadata[-1], '%Y-%m-%dT%H:%M:%SZ')
    resolution = get_resource_resolution(metadata[2])

    return [ extent, thumbnail, creation_date, str(resolution) + ' m/px']


def get_resource_resolution(resource_level):
    
    # Calculate resource resolution
    level_0_resolution = 156412
    return level_0_resolution / 2 ** (resource_level - 8)