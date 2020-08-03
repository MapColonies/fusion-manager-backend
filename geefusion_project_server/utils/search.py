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
        return [False, "Does not exist"]

    # Get project's versions
    versions = get_versions(path)

    # Check if wanted version exists
    if version not in versions:
        return [False, "No such version"]

    return [True, ""]


def get_versions(path):
    bash_command = f"find {path} -maxdepth 1 -iname 'ver*'"
    version_directories = [int(line.decode('utf-8').split(os.sep)[-1].replace("ver", ""))
                           for line in subprocess.check_output(bash_command, shell=True).splitlines()]

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
    return os.sep.join([path, main_xml_name])


def get_version_xml(path, version):

    full_path = path + f'{os.sep}ver{version:03}'

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
    return __get_all_by_name_in_directory_tree__(path, Project, model_type, False, name)


def get_all_resources_by_name_in_directory_tree(path, model_type, name):
    return __get_all_by_name_in_directory_tree__(path, Resource, model_type, True, name)


def __get_directory_content__(directory, model, model_type, check_for_versions):

    extension = get_resource_extension() if model == Resource else get_project_extension()
    if not directory.endswith(os.sep):
        directory += os.sep
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
                versions = get_versions(
                    full_path) if check_for_versions else [1]

                # add dir to results if it has existing versions
                if len(versions) > 0:
                    model_directories.append(name)
            else:
                sub_directories.append(dir)

    return {
        'path': change_root_dir(directory, model_type),
        'directories': sub_directories,
        'items': model_directories
    }


def __get_all_by_name_in_directory_tree__(root_directory, model, model_type, check_for_versions, name):

    extension = get_resource_extension() if model == Resource else get_project_extension()

    # Find all directories with the given name that have a sub directory with a name that answers to the regex ver*
    # %p - full path, %h - full path to containing directory
    bash_command = ' '.join([f"find {root_directory} -name '*{name}*{extension}'",
                             "-type d -execdir find '{}' -maxdepth 1 -name 'ver*' -printf '' \; -printf '%p\\n'"])

    # Execute bash command
    matches = subprocess.check_output(bash_command, shell=True).splitlines()

    # Remove duplicates
    matches = list(dict.fromkeys(matches))

    results = []
    for line in matches:
        line = line.decode('utf-8')
        # Remove . from beginning, and extension from end
        line = line[1:-len(extension)]
        # Set to relative root
        line = change_root_dir(line, model_type)
        line = os.path.join(os.sep, line)
        results.append(line)

    return results
