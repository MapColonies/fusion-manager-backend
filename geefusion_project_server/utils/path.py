import os
from geefusion_project_server.settings import STATIC_ROOT

def cd_path_n_times(path, n=1):

    result = path
    for i in range(n):
        result = result[:result.rfind(os.sep)]
    return result


def get_path_suffix(path):
    return path[path.rfind(os.sep) + 1:]


def get_file_name_from_path(path):
    return path.split(os.sep)[-1].split(".")[0]


def change_root_dir(path, parent_dir_name):
    return path.split(parent_dir_name)[1]


def exists_in_staticfiles(path):
    return os.path.isfile(os.path.join(STATIC_ROOT, path))


def combine_to_path(*strings):
    fixed_paths = [os.sep]
    fixed_paths.extend([ string.strip(os.sep) for string in strings ])
    return os.path.join(*fixed_paths)