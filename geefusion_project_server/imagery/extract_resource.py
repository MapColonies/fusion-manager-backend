import json
import os
from .models import Resource
from datetime import datetime
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml, get_directory_in_directory_tree
from django.core.files.base import ContentFile
from .gee_paths import get_assets_path, get_imagery_resources_path
from .extensions import get_resource_extension
from .string_utils import cd_path_n_times, get_path_suffix

ASSETS_PATH = get_assets_path()
RESOURCE_PATH = get_imagery_resources_path()


def get_resource(path, version, name=None):

    if name == None:
        name = path.split("=")[0].split("/")[-1].split(".")[0]

    # Check if resource exists in DB
    query_set = Resource.objects.filter(name=name, version=version)

    if len(query_set) > 0:
        data = query_set[0]
        resource = Resource(data.name, data.version, data.extent, data.thumbnail, data.takenAt, data.level, data.resolution)
        resource.save()
        return [resource, '']
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    
    if not ans:
        return [None, reason]
    
    # Get resource xml
    xml_path = get_version_xml(path, version)

    extent, thumbnail, creation_date, level, resolution = get_resource_data(xml_path)

    # Create resource object
    resource = Resource(name=name, version=version, extent=extent, takenAt=creation_date, level=level, resolution=resolution)
    # Save thumbnail
    resource.thumbnail.save(thumbnail[0], thumbnail[1])
    # Save resource
    resource.save()
    return [resource, '']


def get_resource_by_name(name, version):
    extension = get_resource_extension()
    path = get_directory_in_directory_tree(RESOURCE_PATH, name, extension)
    #path = RESOURCE_PATH + name + extension
    if path == None:
        return [None, 'No such resource']

    return get_resource(path, version, name=name)


def get_resource_data(xml_path):

    # Get resource metadata
    json = XMLConverter.convert(xml_path)
    metadata = json["meta"]["item"]

    preview_path = ASSETS_PATH + metadata[-2]

    # If the folder was moved, find paths by relative location
    if not os.path.exists(ASSETS_PATH + preview_path):
        preview_path = relatively_get_preview_path(preview_path, xml_path)

    # Read thumbnail
    with open(preview_path, 'rb') as file:
        thumbnail = [metadata[-2], ContentFile(file.read())]
    
    # Get the remaining metadata
    extent = str(metadata[1])
    creation_date = datetime.strptime(metadata[-1], '%Y-%m-%dT%H:%M:%SZ')
    level = metadata[2] - 8
    resolution = get_resource_resolution(level)

    return [ extent, thumbnail, creation_date, level, str(resolution) + ' m/px']


def relatively_get_preview_path(original_preview_path, xml_path):

    # Get version directory name from original path
    version_dir = get_path_suffix(cd_path_n_times(original_preview_path, 1))
    
    # Go up in path 2 times
    preview_path = cd_path_n_times(xml_path, 2)

    # Attach wanted suffix
    preview_path += f'/product.kia/{version_dir}/preview.png'

    return preview_path


def get_resource_resolution(resource_level):
    # Calculate resource resolution
    LEVEL_0_RESOLUTION = 156412
    return LEVEL_0_RESOLUTION / 2 ** resource_level