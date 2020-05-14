import os
import subprocess
import json
# from geefusion_project_server.projects.models import Project
from extract_resource import extract_resource
from datetime import datetime
from xmlconverter import XMLConverter
from search import exists_with_version, get_version_xml

with open("./config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
PROJECTS_PATH = ASSETS_PATH + "Projects/"
# RESOURCE_PATH = ASSETS_PATH + "Resources/"
IMAGERY_PATH = PROJECTS_PATH + "Imagery/"

def get_project(path, version):
    
    # Check if project exists in the wanted version
    ans, reason = exists_with_version(path, version)
    if not ans:
        print(reason)
        return None
    
    # Get project xml
    xml_path = get_version_xml(path, version)
    print(xml_path)
    
    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get project resorce paths
    resource_paths = get_project_resorce_paths(json)
    
    # Get project resources
    splitted_paths = [ split_resource_path(file) for file in resource_paths]
    resources = [extract_resource(file, version, get_resource_resolution(json, file)) for file, version in splitted_paths]

    # return Project("name", version, resources)


# def get_project_versions(path_to_project):
#     bash_command = f"find {path_to_project} -maxdepth 1 -iname 'ver*'"
#     return [ int(line.decode('utf-8').split('/')[-1].replace("ver", "")) for line in subprocess.check_output(bash_command, shell=True).splitlines() ]
    

def get_project_resorce_paths(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ ASSETS_PATH + resources_path for resources_path in inputs ]
    
    # for path in inputs:
    #     full_path = assets_path + path
    #     print(get_creation_time(full_path))


def split_resource_path(path):
    resource_path, version = path.split("?")
    version = int(version.split("=")[1])
    return resource_path, version


def get_resource_resolution(project_main_json, resourve_full_path):

    resourve_relative_path = resourve_full_path.split("assets/")[1]
    
    # Get resource level
    resource_level = [ metadata["maxlevel"] for metadata in project_main_json["config"]["insets"]["inset"] if resourve_relative_path in metadata["dataAsset"] ][0]
    
    # Calculate resource resolution
    level_0_resolution = 156412
    return level_0_resolution / 2 ** (resource_level - 8)


# Test
# projects = [ f.name for f in os.scandir(IMAGERY_PATH) if f.is_dir() ]
# get_project(IMAGERY_PATH + projects[0], 1)