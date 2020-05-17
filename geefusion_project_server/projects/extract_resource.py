import json
from .models import Resource
from datetime import datetime
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml
# import base64
from django.core.files.base import ContentFile

with open("projects/config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
RESOURCE_PATH = ASSETS_PATH + "Resources/Imagery/"


def get_resource(path, version):

    resource_name = path.split("=")[0].split("/")[-1].split(".")[0]

    # Check if resource exists in DB
    query_set = Resource.objects.filter(name=resource_name, version=version)

    if len(query_set) > 0:
        data = query_set[0]
        resource = Resource(data.name, data.version, data.extent, data.thumbnail, data.takenAt, data.level, data.resolution)
        resource.save()
        return [resource, '']
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        print(reason, path)
        return [None, reason]
    
    # Get resource xml
    xml_path = get_version_xml(path, version)

    extent, thumbnail, creation_date, level, resolution = get_resource_data(xml_path)

    # Create resource object
    resource = Resource(name=resource_name, version=version, extent=extent, takenAt=creation_date, level=level, resolution=resolution)
    # Save thumbnail
    resource.thumbnail.save(thumbnail[0], thumbnail[1])
    # Save resource
    resource.save()
    return [resource, '']


def get_resource_by_name(name, version):
    path = RESOURCE_PATH + name
    return get_resource(path, version)


def get_resource_data(xml_path):
    # Get resource metadata
    json = XMLConverter.convert(xml_path)
    metadata = json["meta"]["item"]

    # Read thumbnail
    with open(ASSETS_PATH + metadata[-2], 'rb') as file:
        thumbnail = [metadata[-2], ContentFile(file.read())]
    
    # Get the remaining metadata
    extent = str(metadata[1])
    creation_date = datetime.strptime(metadata[-1], '%Y-%m-%dT%H:%M:%SZ')
    level = metadata[2] - 8
    resolution = get_resource_resolution(level)

    return [ extent, thumbnail, creation_date, level, str(resolution) + ' m/px']


def get_resource_resolution(resource_level):
    # Calculate resource resolution
    LEVEL_0_RESOLUTION = 156412
    return LEVEL_0_RESOLUTION / 2 ** resource_level