from imagery.models import Project, Resource
from utils.constants.extensions import get_resource_extension, get_project_extension
from config.gee_paths import get_imagery_projects_path, get_imagery_resources_path
from utils.search import get_versions

IMAGERY_PROJECT_PATH = get_imagery_projects_path()
RESOURCE_PATH = get_imagery_resources_path()


def get_latest_version(path):
    versions = get_versions(path)
    # If the resource has no versions
    if len(versions) == 0:
        return 0
    return max(versions)


# def get_path(model, path, name):

    # extension = get_project_extension() if model == Project else get_resource_extension()
    # path = __get_path_from_db__(model, path, name)

    # if not path:
    #     root = IMAGERY_PROJECT_PATH if model == Project else RESOURCE_PATH
    #     path = get_directory_in_directory_tree(root, name, extension)

    # return path


# def __get_path_from_db__(model, path, name):
#     query_set = model.objects.filter(name=name, path=path)
#     print(len(query_set))
#     return query_set[0].path if len(query_set) > 0 else None