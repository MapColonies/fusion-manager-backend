import json
from .models import Project, ProjectResources
from .extract_resource import get_resource
from .xmlconverter import XMLConverter
from .search import exists_with_version, get_version_xml

with open("projects/config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
# PROJECTS_PATH = ASSETS_PATH + "Projects/"
# IMAGERY_PATH = PROJECTS_PATH + "Imagery/"

def get_project(path, version):

    project_name = path.split("=")[0].split("/")[-1].split(".")[0]

    # Check if resource exists in DB
    query_set = Project.objects.filter(name=project_name, version=version)

    if len(query_set) > 0:
        data = query_set[0]
        return [Project(data.name, data.version), '']
    
    # Check if project exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        print(reason)
        return [None, reason]
    
    # Get project xml
    xml_path = get_version_xml(path, version)
    print(xml_path)
    
    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get project resorce paths
    resource_paths = get_project_resorce_paths(json)
    
    # Get project resources
    splitted_paths = [ split_resource_path(file) for file in resource_paths]
    resources = [get_resource(file, version)[0] for file, version in splitted_paths]

    project = Project(name=project_name, version=version)
    project.save()

    for resource in resources:
        project.resources.add(resource)

    return [project, ""]
   

def get_project_resorce_paths(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ ASSETS_PATH + resources_path for resources_path in inputs ]


def split_resource_path(path):
    resource_path, version = path.split("?")
    version = int(version.split("=")[1])
    return resource_path, version