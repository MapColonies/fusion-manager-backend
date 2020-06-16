def cd_path_n_times(path, n):

    result = path
    for i in range(n):
        result = result[:result.rfind('/')]
    return result


def get_path_suffix(path):

    return path[path.rfind('/') + 1:]