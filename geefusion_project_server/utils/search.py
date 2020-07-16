import os
import subprocess
from imagery.models import Resource, Project
from utils.constants.extensions import get_project_extension, get_resource_extension
from utils.constants.filenames import get_main_xml_name, get_version_xml_name
from utils.path import change_root_dir, combine_to_path
from .xmlconverter import XMLConverter

def exists_with_version(path, version):

    # Check if project exists
    if not os.path.isdir(path):
        return [ False, "Does not exist" ]
    
    # Get project's versions
    versions = get_versions(path)
    
    # Check if wanted version exists
    if version not in versions:
        return [ False, "No such version" ]
    
    return [ True, "" ]


def get_versions(path):
    bash_command = f"find {path} -maxdepth 1 -iname 'ver*'"
    version_directories = [ int(line.decode('utf-8').split('/')[-1].replace("ver", "")) for line in subprocess.check_output(bash_command, shell=True).splitlines() ]

    # Get only valid versions
    valid_versions = []
    for version in version_directories:

        # Get version's state
        version_xml = get_version_xml(path, version)
        json = XMLConverter.convert(version_xml)
        state = json["state"]
        
        # Check state
        if state == "Succeeded":
            valid_versions.append(version)

    return valid_versions


def get_main_xml(path):
    main_xml_name = get_main_xml_name()
    return '/'.join([path, main_xml_name])


def get_version_xml(path, version):

    full_path = path + f'/ver{version:03}'
    
    # Get version xml
    xml_name = get_version_xml_name()
    bash_command = f"find {full_path} -maxdepth 1 -iname {xml_name}"
    xml_list = subprocess.check_output(bash_command, shell=True).splitlines()
    return xml_list[0].decode("utf-8")


def get_all_in_directory(path, model, model_type):

    if not os.path.isdir(path):
        path = change_root_dir(path, 'Imagery')
        return f'The path {path} is not a valid directory.'
    
    if model == Resource:
        return __get_directory_content__(path, Resource, model_type, True)
    
    return __get_directory_content__(path, Project, model_type, False)


def get_all_projects_by_name_in_directory_tree(path, model_type, name):
    # return __get_all_in_directory_tree__(root, Project, False)
    return __get_all_by_name_in_directory_tree__(path, Project, model_type, False, name)


def get_all_resources_by_name_in_directory_tree(path, model_type, name):
    # return __get_all_in_directory_tree__(root, Resource, True)
    return __get_all_by_name_in_directory_tree__(path, Resource, model_type, True, name)


# def get_directory_in_directory_tree(root_directory, name, extension):

#     full_name = name + extension

#     for root, dirs, files in os.walk(root_directory, topdown=True):
#         if full_name in dirs:
#             if not root.endswith('/'): root += '/'
#             return root + full_name
    
#     # Not found
#     return None


def __get_directory_content__(directory, model, model_type, check_for_versions):

    extension = get_resource_extension() if model == Resource else get_project_extension()
    if not directory.endswith('/'): directory += '/'
    model_directories = []
    sub_directories = []

    # find wanted directories
    for content in os.listdir(directory):

        if os.path.isdir(directory + content):
            dir = content

            # Check for specific directories
            if dir.endswith(extension):

                # remove extension
                name = dir[:-len(extension)]

                full_path = directory + dir
                versions = get_versions(full_path) if check_for_versions else [1]

                # add dir to results if it has existing versions
                if len(versions) > 0:
                    model_directories.append(name)
            else:
                sub_directories.append(dir)
    
    res = {
        'path': change_root_dir(directory, model_type),
        'directories': sub_directories
    }

    # Set model directories part of result
    model_name = 'resources' if model == Resource else 'projects'
    res[model_name] = model_directories

    return res


# def __get_all_in_directory_tree__(root_directory, model, check_for_versions):

#     wanted_directories = []
#     extension = get_resource_extension() if model == Resource else get_project_extension()
#     model_root_dir_name = 'Resource' if model == Resource else 'Project'

#     for root, dirs, files in os.walk(root_directory, topdown=True):

#         # Go over copy of dir list (because changes are made while in loop)
#         dirs_copy = dirs.copy()

#         if not root.endswith('/'): root += '/'

#         # find wanted directories
#         for dir in dirs_copy:

#             # Check for specific directories
#             if dir.endswith(extension):

#                 # remove extension
#                 name = dir[:-len(extension)]

#                 full_path = root + dir
#                 versions = get_versions(full_path) if check_for_versions else [1]

#                 # add dir to results if it has existing versions
#                 if len(versions) > 0:
#                     wanted_directories.append({
#                         'name': name,
#                         'path': change_root_dir(full_path, model_root_dir_name)
#                     })

#                 # remove for directory list so walk wouldn't go in
#                 dirs.remove(dir)
    
#     return wanted_directories


def __get_all_by_name_in_directory_tree__(root_directory, model, model_type, check_for_versions, name):

    extension = get_resource_extension() if model == Resource else get_project_extension()

    # Find all directories with the given name that have a sub directory with a name that answers to the regex ver*
    bash_command = ' '.join([ f"find {root_directory} -name '{name}*{extension}'", "-type d -execdir find '{}' -maxdepth 1 -name 'ver*' -printf '' \; -printf '%h\\n'" ])

    # Execute bash command
    matches = subprocess.check_output(bash_command, shell=True).splitlines()

    # Remove duplicates
    matches = list(dict.fromkeys(matches))

    # Decode lines to utf-8, remove "./" from the beginning of the path and set full path
    # return [ os.path.join(change_root_dir(line.decode('utf-8')[1:], model_type), name) for line in matches ]

    results = []
    for line in matches:

        line = line.decode('utf-8')
        line = line[1:]
        line = change_root_dir(line, model_type)
        line = os.path.join('/', line)
        results.append(line)

    return results