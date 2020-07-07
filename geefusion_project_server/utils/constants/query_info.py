from imagery.models import Resource, Project


def get_query_info(fields, check_arr, model):
    model_name = 'Resource' if model == Resource else 'Project'
    query_info = []

    for field, check in zip(fields, check_arr):
        query_info.append(__get_query_info_by_name__(field, check, model_name))
    
    return query_info


def __get_query_info_by_name__(name, check, model_name):

    if name == 'name': return __get_name_query_info__(check, model_name)
    elif name == 'path': return __get_path_query_info__(check, model_name)
    elif name == 'version': return __get_version_query_info__(check, model_name)
    else: return {}


def __get_name_query_info__(check, model_name):
    return {
        'name': 'name',
        'check': check,
        'default': '',
        'error_message': f"{model_name} name wasn't provided"
    }


def __get_path_query_info__(check, model_name):
    return {
        'name': 'path',
        'check': check,
        'default': '',
        'error_message': f"{model_name} path wasn't provided"
    }


def __get_version_query_info__(check, model_name):
    return {
        'name': 'version',
        'check': check,
        'default': 'latest',
        'error_message': f"{model_name} version wasn't provided"
    }