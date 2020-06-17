import json
import os
from .models import Resource
from datetime import datetime
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml, get_directory_in_directory_tree, get_versions
from django.core.files.base import ContentFile
from .gee_paths import get_assets_path, get_imagery_resources_path
from .extensions import get_resource_extension
from .string_utils import cd_path_n_times, get_path_suffix, get_file_name_from_path
from .model_utils import get_path

ASSETS_PATH = get_assets_path()
RESOURCE_PATH = get_imagery_resources_path()


def get_resource(path, version, name=None):
    
    if name == None:
        name = get_file_name_from_path(path)

    # Check if resource exists in DB
    query_set = Resource.objects.filter(name=name, version=version)
    
    if len(query_set) > 0:
        data = query_set[0]
        resource = Resource(data.name, data.version, data.path, data.extent, data.thumbnail, data.takenAt, data.level, data.resolution)
        resource.save()
        return [resource, '']
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    
    if not ans:
        return [None, reason]
    
    # Get resource xml
    xml_path = get_version_xml(path, version)
    
    data, reason = __get_resource_data__(xml_path)
    if not data:
        return [None, reason]

    extent, thumbnail, creation_date, level, resolution = data

    # Create resource object
    resource = Resource(name=name, version=version, path=path, extent=extent, takenAt=creation_date, level=level, resolution=resolution)
    # Save thumbnail
    resource.thumbnail.save(thumbnail[0], thumbnail[1])
    # Save resource
    resource.save()
    return [resource, '']


def get_resource_by_name(name, version='latest'):
    extension = get_resource_extension()
    path = get_directory_in_directory_tree(RESOURCE_PATH, name, extension)
    
    if path == None:
        return [None, 'No such resource']
    
    if version == 'latest':
        versions = get_versions(path)

        # If the resource has no versions
        if len(versions) == 0:
            return [None, 'Resource has no versions']

        version = max(versions)
    
    return get_resource(path, version, name=name)


def __get_resource_data__(xml_path):

    # Get resource metadata
    json = XMLConverter.convert(xml_path)
    metadata = json["meta"]["item"]

    preview_path = ASSETS_PATH + metadata[-2]

    # If the folder was moved, find paths by relative location
    if not os.path.exists(ASSETS_PATH + preview_path):
        preview_path = __relatively_get_preview_path__(preview_path, xml_path)

    # Read thumbnail
    with open(preview_path, 'rb') as file:
        thumbnail = [metadata[-2], ContentFile(file.read())]
    
    # Get the remaining metadata
    extent = str(metadata[1])

    date_taken = metadata[-1]
    resource_name = get_file_name_from_path(json["name"])
    if date_taken == '0000-00-00T00:00:00Z':
        return [None, f"Resource date is invalid, please modify the following resource's date: {resource_name}"]

    creation_date = datetime.strptime(date_taken, '%Y-%m-%dT%H:%M:%SZ')
    level = metadata[2] - 8
    
    resolution = __get_resource_resolution__(level)

    return [[ extent, thumbnail, creation_date, level, str(resolution) + ' m/px'], '']


def get_resource_versions(name):
    path = get_path(Resource, name)
    return get_versions(path)


def __relatively_get_preview_path__(original_preview_path, xml_path):

    # Get version directory name from original path
    version_dir = get_path_suffix(cd_path_n_times(original_preview_path, 1))
    
    # Go up in path 2 times
    preview_path = cd_path_n_times(xml_path, 2)

    # Attach wanted suffix
    preview_path += f'/product.kia/{version_dir}/preview.png'

    return preview_path


def __get_resource_resolution__(resource_level):
    # Calculate resource resolution
    LEVEL_0_RESOLUTION = 156412
    return LEVEL_0_RESOLUTION / 2 ** resource_level