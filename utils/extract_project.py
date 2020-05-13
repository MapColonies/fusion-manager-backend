import os
import subprocess
import json
# from geefusion_project_server.projects.models import Project
from extract_resource import extract_resource
from datetime import datetime
from xmlconverter import XMLConverter

with open("config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
PROJECTS_PATH = ASSETS_PATH + "Projects/"
# RESOURCE_PATH = ASSETS_PATH + "Resources/"
IMAGERY_PATH = PROJECTS_PATH + "Imagery/"

def get_project(path, version):
    
    # Check if project exists
    if not os.path.isdir(path):
        print("Project does not exist")
        return []
    
    # Get project's versions
    versions = get_project_versions(path)
    
    # Check if wanted version exists
    if version not in versions:
        print("Project has no such version")
        return None
    
    full_path = path + f'/ver{version:03}'
    
    # Get project xml
    bash_command = f"find {full_path} -maxdepth 1 -iname 'khasset*.xml'"
    xml_list = subprocess.check_output(bash_command, shell=True).splitlines()
    xml_path = xml_list[0]
    
    # Convert xml to json
    json = XMLConverter.convert(xml_path)

    # Get project resorce paths
    resource_paths = get_project_resorce_paths(json)
    
    # Get project resources
    splitted_paths = [ split_resource_path(file) for file in resource_paths]
    resources = [extract_resource(file, version) for file, version in splitted_paths]

    # return Project("name", version, resources)


def get_project_versions(path_to_project):
    bash_command = f"find {path_to_project} -maxdepth 1 -iname 'ver*'"
    return [ int(line.decode('utf-8').split('/')[-1].replace("ver", "")) for line in subprocess.check_output(bash_command, shell=True).splitlines() ]
    

def get_project_resorce_paths(json):
    inputs = json["inputs"]["input"]
    inputs = inputs if isinstance(inputs, list) else [inputs]
    return [ ASSETS_PATH + resources_path for resources_path in inputs ]
    
    # for path in inputs:
    #     full_path = assets_path + path
    #     print(get_creation_time(full_path))


def split_resource_path(path):
    resource_path, version = path.split("?")
    version = version.split("=")[1]
    return resource_path, version

# Test
projects = [ f.name for f in os.scandir(IMAGERY_PATH) if f.is_dir() ]
get_project(IMAGERY_PATH + projects[0], 1)