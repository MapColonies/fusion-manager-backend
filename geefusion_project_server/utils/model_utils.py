from imagery.models import Project, Resource
from utils.constants.extensions import get_resource_extension, get_project_extension
from config.gee_paths import get_imagery_projects_path, get_imagery_resources_path
from .search import get_directory_in_directory_tree, get_versions

IMAGERY_PROJECT_PATH = get_imagery_projects_path()
RESOURCE_PATH = get_imagery_resources_path()


def get_path(model, name):

    extension = get_project_extension() if model == Project else get_resource_extension()
    path = __get_path__(model, name)

    if not path:
        root = IMAGERY_PROJECT_PATH if model == Project else RESOURCE_PATH
        path = get_directory_in_directory_tree(root, name, extension)

    return path


def __get_path__(model, name):
    query_set = model.objects.filter(name=name)
    return query_set[0].path if len(query_set) > 0 else None