import json
from .models import Project, ProjectResources
from .extract_resource import get_resource
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml, get_directory_in_directory_tree
from .gee_paths import get_assets_path, get_imagery_projects_path
from .extensions import get_project_extension

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
    resource_paths = get_project_resorce_paths(json)
    
    # Get project resources
    splitted_paths = [ split_resource_path(file) for file in resource_paths]
    #resources = [get_resource(file, version)[0] for file, version in splitted_paths]

    resources = []
    for file, version in splitted_paths:

        resource, reason = get_resource(file, version)
        if not resource:
            return [None, f'Failed getting resource {name}. Error message: {reason}. Resource directory was probably moved or deleted.']
        
        resources.append(resource)

    project = Project(name=name, version=version)
    project.save()

    for resource in resources:
        project.resources.add(resource)

    return [project, '']


def get_project_by_name(name, version):
    extension = get_project_extension()
    path = get_directory_in_directory_tree(IMAGERY_PROJECT_PATH, name, extension)
    #path = get_imagery_projects_path() + name + extension
    print(path)
    if not path:
        return [None, 'No such project']
    
    return get_project(path, name, version)


def get_project_resorce_paths(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ ASSETS_PATH + resources_path for resources_path in inputs ]


def split_resource_path(path):
    resource_path, version = path.split("?")
    version = int(version.split("=")[1])
    return resource_path, version