import os
import subprocess

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
    print(path)
    bash_command = f"find {path} -maxdepth 1 -iname 'ver*'"
    return [ int(line.decode('utf-8').split('/')[-1].replace("ver", "")) for line in subprocess.check_output(bash_command, shell=True).splitlines() ]


def get_version_xml(path, version):

    full_path = path + f'/ver{version:03}'
    
    # Get version xml
    bash_command = f"find {full_path} -maxdepth 1 -iname 'khasset*.xml'"
    xml_list = subprocess.check_output(bash_command, shell=True).splitlines()
    return xml_list[0].decode("utf-8")


def get_all_projects_in_directory_tree(root):
    return __get_all_in_directory_tree__(root, '.kiproject')


def get_all_resources_in_directory_tree(root):
    return __get_all_in_directory_tree__(root, '.kiasset')


def get_directory_in_directory_tree(root_directory, name, extension):

    full_name = name + extension

    for root, dirs, files in os.walk(root_directory, topdown=True):
        if full_name in dirs:
            return root + '/' + full_name
    
    # Not found
    return None


def __get_all_in_directory_tree__(root_directory, extension):

    wanted_directories = []

    for root, dirs, files in os.walk(root_directory, topdown=True):

        # find wanted directories
        wanted_sub_directories = [ dir for dir in dirs if dir.endswith(extension) ]

        for dir in wanted_sub_directories:
            # remove extension
            name = dir[:-len(extension)]

            # add dir to results
            wanted_directories.append(name)

            # remove for directory list so walk wouldn't go in
            dirs.remove(dir)
    
    return wanted_directories