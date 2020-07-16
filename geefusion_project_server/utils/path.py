import os
from geefusion_project_server.settings import STATIC_ROOT

def cd_path_n_times(path, n=1):

    result = path
    for i in range(n):
        result = result[:result.rfind('/')]
    return result


def get_path_suffix(path):
    return path[path.rfind('/') + 1:]


def get_file_name_from_path(path):
    return path.split("/")[-1].split(".")[0]


def change_root_dir(path, parent_dir_name):
    return path.split(parent_dir_name)[1]


def exists_in_staticfiles(path):
    return os.path.isfile(STATIC_ROOT + '/' + path)


def combine_to_path(*strings):
    fixed_paths = ['/']
    fixed_paths.extend([ string.strip('/') for string in strings ])
    return os.path.join(*fixed_paths)