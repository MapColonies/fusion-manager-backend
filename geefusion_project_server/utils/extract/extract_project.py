import json
import os
from imagery.models import Project, ProjectResources
from .extract_resource import get_resource
from utils.xmlconverter import XMLConverter
from utils.search import exists_with_version, get_versions, get_version_xml, get_main_xml
from config.gee_paths import get_assets_path, get_imagery_projects_path
from utils.constants.extensions import get_project_extension
from utils.path import get_path_suffix, change_root_dir
from utils.model import get_latest_version

ASSETS_PATH = get_assets_path()
IMAGERY_PROJECT_PATH = get_imagery_projects_path()


def get_project(path, name, version='latest'):

    if name not in path:
        path += f'{name}{get_project_extension()}'

    # Check that the given path is a directory
    if not os.path.isdir(path):
        return [None, 'Does not exist']

    if version == 'latest':
        version = get_latest_version(path)

    if version != 0:
        # Check if resource exists in DB
        query_set = Project.objects.filter(
            name=name, version=version, path=path)

        if len(query_set) > 0:
            project = query_set[0]
            return [project, '']

        # Check if project exists in the wanted version
        ans, reason = exists_with_version(path, version)
        if not ans:
            return [None, reason]

    # Get project xml
    xml_path = get_version_xml(
        path, version) if version != 'latest' else get_main_xml(path)
    # Get project resources
    resources, reason = __get_project_resources__(xml_path)
    if not resources:
        return [None, reason]

    project = Project.objects.create(name=name, version=version, path=path)

    for resource in resources:
        project.resources.add(resource)

    return [project, '']


def get_project_versions(path, name):
    return get_versions(path)


def __get_project_resources__(xml_path):

    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get project resorce paths
    resource_paths = __get_project_resorce_paths__(json)

    # Get project resources
    splitted_paths = [__split_resource_path__(file) for file in resource_paths]

    resources = []
    for file, version in splitted_paths:
        resource, mask, reason = get_resource(file, version)
        if not resource:
            error_message = f'Failed getting resource {get_path_suffix(file)}. Error message: {reason}.'
            if reason == 'Does not exist':
                error_message += ' Resource may have been moved or deleted.'
            return [None, error_message]

        resources.append(resource)

    return [resources, '']


def __get_project_resorce_paths__(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ASSETS_PATH + resources_path for resources_path in inputs]


def __split_resource_path__(path):
    if '?' in path:
        resource_path, version = path.split("?")
        version = int(version.split("=")[1])
    else:
        resource_path = path
        version = 'latest'
    return resource_path, version
