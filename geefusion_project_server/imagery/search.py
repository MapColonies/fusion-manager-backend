import os
import subprocess
from .extensions import get_project_extension, get_resource_extension
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


def get_version_xml(path, version):

    full_path = path + f'/ver{version:03}'
    
    # Get version xml
    bash_command = f"find {full_path} -maxdepth 1 -iname 'khasset*.xml'"
    xml_list = subprocess.check_output(bash_command, shell=True).splitlines()
    return xml_list[0].decode("utf-8")


def get_all_projects_in_directory_tree(root):
    extension = get_project_extension()
    return __get_all_in_directory_tree__(root, extension, False)


def get_all_resources_in_directory_tree(root):
    extension = get_resource_extension()
    return __get_all_in_directory_tree__(root, extension, True)


def get_directory_in_directory_tree(root_directory, name, extension):

    full_name = name + extension

    for root, dirs, files in os.walk(root_directory, topdown=True):
        if full_name in dirs:
            if not root.endswith('/'): root += '/'
            return root + full_name
    
    # Not found
    return None


def __get_all_in_directory_tree__(root_directory, extension, check_for_versions):

    wanted_directories = []
    print(root_directory)

    for root, dirs, files in os.walk(root_directory, topdown=True):

        # Go over copy of dir list (because changes are made while in loop)
        dirs_copy = dirs.copy()

        # find wanted directories
        for dir in dirs_copy:

            # Check for specific directories
            if dir.endswith(extension):

                # remove extension
                name = dir[:-len(extension)]

                if not root.endswith('/'): root += '/'
                full_path = root + dir
                versions = get_versions(full_path)

                # add dir to results if it has existing versions
                if len(versions) > 0:
                    wanted_directories.append(name)

                # remove for directory list so walk wouldn't go in
                dirs.remove(dir)

        # for dir in wanted_sub_directories:
        #     # remove extension
        #     name = dir[:-len(extension)]

        #     # add dir to results
        #     wanted_directories.append(name)

        #     # remove for directory list so walk wouldn't go in
        #     dirs.remove(dir)
    
    return wanted_directories