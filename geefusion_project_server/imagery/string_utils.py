def cd_path_n_times(path, n):

    result = path
    for i in range(n):
        result = result[:result.rfind('/')]
    return result


def get_path_suffix(path):

    return path[path.rfind('/') + 1:]


def get_file_name_from_path(path):

    return path.split("/")[-1].split(".")[0]