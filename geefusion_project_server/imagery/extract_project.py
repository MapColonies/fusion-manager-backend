import json
import os
from .models import Project, ProjectResources
from .extract_resource import get_resource
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_versions, get_version_xml, get_directory_in_directory_tree
from .gee_paths import get_assets_path, get_imagery_projects_path
from .extensions import get_project_extension
from .model_utils import get_path
from .string_utils import get_path_suffix

ASSETS_PATH = get_assets_path()
IMAGERY_PROJECT_PATH = get_imagery_projects_path()

def get_project(path, name, version):

    # Check if resource exists in DB
    query_set = Project.objects.filter(name=name, version=version)

    if len(query_set) > 0:
        data = query_set[0]
        return [Project(data.name, data.version), '']
    
    # Check if project exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        return [None, reason]
    
    # Get project xml
    xml_path = get_version_xml(path, version)
    
    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get project resorce paths
    resource_paths = __get_project_resorce_paths__(json)
    
    # Get project resources
    splitted_paths = [ __split_resource_path__(file) for file in resource_paths]
    #resources = [get_resource(file, version)[0] for file, version in splitted_paths]

    resources = []
    for file, version in splitted_paths:

        resource, reason = get_resource(file, version)
        if not resource:
            error_message = f'Failed getting resource {get_path_suffix(file)}. Error message: {reason}.'
            if reason == 'Does not exist': error_message += ' Resource may have been moved or deleted.'
            return [None, error_message]
        
        resources.append(resource)

    project = Project(name=name, version=version, path=path)
    project.save()

    for resource in resources:
        project.resources.add(resource)

    return [project, '']


def get_project_by_name(name, version='latest'):
    extension = get_project_extension()
    path = get_directory_in_directory_tree(IMAGERY_PROJECT_PATH, name, extension)
    
    if not path:
        return [None, 'No such project']

    if version == 'latest':
        versions = get_versions(path)
        version = max(versions)
    
    return get_project(path, name, version)


def get_project_versions(name):
    path = get_path(Project, name)
    return get_versions(path)


def __get_project_resorce_paths__(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ ASSETS_PATH + resources_path for resources_path in inputs ]


def __split_resource_path__(path):
    resource_path, version = path.split("?")
    version = int(version.split("=")[1])
    return resource_path, version