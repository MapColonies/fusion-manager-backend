import os

def get_assets_path():

    return os.environ.get('FUSION_PATH', '/gevol/fusion/') + 'assets/'

def get_imagery_resources_path():

    return get_assets_path() + "Resources/Imagery/"

def get_imagery_projects_path():

    return get_assets_path() + "Projects/Imagery/"