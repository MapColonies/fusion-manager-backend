import json
import os
from imagery.models import Resource, Mask
from datetime import datetime
from utils.xmlconverter import XMLConverter
from utils.search import exists_with_version, get_version_xml, get_versions
from django.core.files.base import ContentFile
from config.gee_paths import get_assets_path, get_imagery_resources_path
from utils.constants.extensions import get_resource_extension
from utils.constants.date import default_date
from utils.path import cd_path_n_times, get_path_suffix, get_file_name_from_path, exists_in_staticfiles, change_root_dir
from utils.model import get_latest_version

ASSETS_PATH = get_assets_path()
RESOURCE_PATH = get_imagery_resources_path()


def get_resource(path, version='latest', name=None):

    # Set name if missing
    if name == None:
        name = get_file_name_from_path(path)
    elif name not in path:
        path += f'{name}{get_resource_extension()}'
    
    # Check that the given path is a directory
    if not os.path.isdir(path):
        return [None, None, 'Does not exist']

    # Set version to latest version if requested
    if version == 'latest':
        version = get_latest_version(path)
        # If the resource has no versions
        if version == 0:
            return [None, None, 'Resource has no versions']
    
    # Check if resource exists in DB
    query_set = Resource.objects.filter(name=name, version=version, path=path)
    
    if len(query_set) > 0:
        resource = query_set[0]
        mask = resource.mask
        return [resource, mask, '']
    
    # Check if resource exists in the wanted version
    ans, reason = exists_with_version(path, version)
    
    if not ans:
        return [None, None, reason]
    
    # Get resource xml
    xml_path = get_version_xml(path, version)
    
    data, reason = __get_data__(xml_path)
    if not data:
        return [None, None, reason]
    
    extent, thumbnail, creation_date, level, resolution, mask = data

    # Create resource object
    resource = Resource(name=name, version=version, path=path, extent=extent, taken_at=creation_date, level=level, resolution=resolution, mask=mask)
    
    # Save resource thumbnail
    __save_resource_thumbnail__(resource, thumbnail)
    
    # Save resource
    resource.save()
    return [resource, mask, '']


def __save_resource_thumbnail__(resource, thumbnail):
    thumbnail_original_path = thumbnail[0]
    thumbnail_resource_version = get_path_suffix(cd_path_n_times(thumbnail_original_path))
    thumbnail_data = thumbnail[1]
    thumbnail_path = f'Resources/Imagery/{resource.name}/{thumbnail_resource_version}/preview.png'

    # Check if thumbnail already exists
    if not exists_in_staticfiles(thumbnail_path):
        # Save thumbnail
        resource.thumbnail.save(thumbnail_path, thumbnail_data)
    else:
        # Reference existing thumbnail
        resource.thumbnail.name = 'static/' + thumbnail_path


# def get_resource_by_name(name, version='latest'):
    # path = get_path(Resource, name)

    # if path == None:
    #     return [None, None, 'No such resource']
    
    # return get_resource(path, version, name=name)


def get_resource_image(path, name, version):
    query_set = Resource.objects.filter(name=name, version=version, path=path)
    
    if len(query_set) > 0:
        resource = query_set[0]
        image = resource.thumbnail
        return [image, '']
    
    return [None, 'Image not found']


# def __get_latest_version__(path):
#     versions = get_versions(path)
#     # If the resource has no versions
#     if len(versions) == 0:
#         return 0
#     return max(versions)


def __get_data__(xml_path):
    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get metadata
    metadata, reason = __get_metadata__(xml_path, json)

    if not metadata: return [metadata, reason]
    
    # Get config
    config_data = __get_config_data__(json)
    
    data = []
    data.extend(metadata)
    data.extend(config_data)
    return [data, '']


def __get_metadata__(xml_path, json):

    # Get resource metadata
    metadata = json["meta"]["item"]

    # Check that creation date is valid
    date_taken = metadata[-1]
    resource_name = get_file_name_from_path(json["name"])
    if date_taken == default_date():
        return [None, f"Resource date is invalid, please modify the following resource's date: {resource_name}"]
    
    # Read metadata
    thumbnail = __get_preview__(xml_path, metadata)
    extent = str(metadata[1])
    creation_date = datetime.strptime(date_taken, '%Y-%m-%dT%H:%M:%SZ')
    level = metadata[2] - 8
    resolution = __get_resolution_by_level__(level)

    return [[ extent, thumbnail, creation_date, level, str(resolution) + ' m/px'], '']


def __get_config_data__(json):

    config = json['config']

    no_mask = int(config['nomask']) if 'nomask' in config else 0
    # If no mask is defined
    if no_mask == 1:
        mask = Mask(no_mask=bool(no_mask), feather=100, mode='Mask', band=1, fill_value=-1,
                    threshold=0, hole_size=0, white_fill=0, no_data=None)
        mask.save()
        return [mask]
    
    mask_gen_config = config['maskgenConfig']

    # Get mask gen data
    mask = Mask(
        no_mask=no_mask,
        feather=mask_gen_config['feather'],
        mode=mask_gen_config['mode'],
        band=mask_gen_config['band'],
        fill_value=mask_gen_config['fillvalue'], 
        threshold=mask_gen_config['threshold'],
        hole_size=mask_gen_config['holesize'],
        white_fill=mask_gen_config['whitefill'],
        no_data=mask_gen_config['nodata']
    )
    mask.save()
    return [mask]


def __get_preview__(xml_path, metadata):
    # Get preview's full path
    preview_path = ASSETS_PATH + metadata[-2]

    # If the folder was moved, find paths by relative location
    if not os.path.exists(ASSETS_PATH + preview_path):
        preview_path = __relatively_get_preview_path__(preview_path, xml_path)

    # Read thumbnail
    with open(preview_path, 'rb') as file:
        data = ContentFile(file.read())
    
    return [metadata[-2], data]


def get_resource_versions(path, name):
    return get_versions(path)


def __relatively_get_preview_path__(original_preview_path, xml_path):

    # Get version directory name from original path
    version_dir = get_path_suffix(cd_path_n_times(original_preview_path, 1))
    
    # Go up in path 2 times
    preview_path = cd_path_n_times(xml_path, 2)

    # Attach wanted suffix
    preview_path += f'/product.kia/{version_dir}/preview.png'

    return preview_path


def __get_resolution_by_level__(resource_level):
    # Calculate resource resolution
    LEVEL_0_RESOLUTION = 156412
    return LEVEL_0_RESOLUTION / float(2 ** resource_level)