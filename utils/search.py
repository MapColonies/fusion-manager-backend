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
    bash_command = f"find {path} -maxdepth 1 -iname 'ver*'"
    return [ int(line.decode('utf-8').split('/')[-1].replace("ver", "")) for line in subprocess.check_output(bash_command, shell=True).splitlines() ]


def get_version_xml(path, version):

    full_path = path + f'/ver{version:03}'
    
    # Get version xml
    bash_command = f"find {full_path} -maxdepth 1 -iname 'khasset*.xml'"
    xml_list = subprocess.check_output(bash_command, shell=True).splitlines()
    return xml_list[0]