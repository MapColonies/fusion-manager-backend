import os
import subprocess
from xmlconverter import XMLConverter

# assets_path = "/opt/google/share/tutorials/fusion/assets/"
assets_path = "C:/Users/Rasberey/Documents/fusion/assets/"
projects_path = assets_path + "Projects/"
resources_path = assets_path + "Resources/"
imagery_path = projects_path + "Imagery/"

projects = [ f.name for f in os.scandir(imagery_path) if f.is_dir() ]
# projects = [ f.name.split('.')[0] for f in os.scandir(imagery_path) if f.is_dir() ]

print("Projects: " + str(projects))

def read_main_xml(path):

    xml_list = [ line for line in subprocess.check_output(f"find {path} -maxdepth 1 -iname 'khasset*.xml'", shell=True).splitlines() ]
    print(xml_list)

    json = XMLConverter.convert(xml_list[0])
    print(json)

    get_project_inputs(json)

def get_project_inputs(json):
    inputs = json["inputs"]["input"]
    print(inputs)

read_main_xml(imagery_path + projects[0])